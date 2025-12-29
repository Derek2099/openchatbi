"""System prompt templates and business configuration."""

import importlib.resources

from openchatbi import config

# Global cache variables for lazy loading (only for file I/O operations)
_dialect_rules_cache = None
_domain_specific_cache = None
_agent_prompt_template_cache = None
_extraction_prompt_template_cache = None
_table_selection_prompt_template_cache = None
_text2sql_prompt_template_cache = None
_visualization_prompt_template_cache = None
_summary_prompt_template_cache = None


def get_basic_knowledge():
    """Get basic knowledge from config."""
    try:
        return config.get().bi_config.get("basic_knowledge_glossary", "")
    except ValueError:
        return ""


def get_data_warehouse_introduction():
    """Get data warehouse introduction from config."""
    try:
        return config.get().bi_config.get("data_warehouse_introduction", "")
    except ValueError:
        return ""


def get_agent_extra_tool_use_rule():
    """Get agent extra tool use rule from config."""
    try:
        return config.get().bi_config.get("extra_tool_use_rule", "")
    except ValueError:
        return ""


def get_organization():
    """Get organization from config."""
    try:
        return config.get().organization
    except ValueError:
        return "The Company"


def get_dialect_rules():
    """Get SQL dialect rules with lazy loading and caching."""
    global _dialect_rules_cache
    if _dialect_rules_cache is None:
        dialect_dir = importlib.resources.files("openchatbi.prompts.sql_dialect")
        _dialect_rules_cache = {}

        for item in dialect_dir.iterdir():
            if item.is_file() and item.name.endswith(".md"):
                dialect_name = item.name[:-3]
                with item.open() as f:
                    prompt = f.read()
                    _dialect_rules_cache[dialect_name] = prompt
    return _dialect_rules_cache


def get_domain_specific_docs():
    """Get domain-specific documentation files with lazy loading and caching.
    
    Returns:
        dict: A dictionary mapping domain file names (without .md extension) to their content.
              Example: {'dm_domain': '...', 'ae_domain': '...', 'sdtm_glossary': '...'}
    """
    global _domain_specific_cache
    if _domain_specific_cache is None:
        domain_dir = importlib.resources.files("openchatbi.prompts.domain_specific")
        _domain_specific_cache = {}

        for item in domain_dir.iterdir():
            if item.is_file() and item.name.endswith(".md"):
                domain_name = item.name[:-3]
                with item.open("r", encoding="utf-8") as f:
                    content = f.read()
                    _domain_specific_cache[domain_name] = content
    return _domain_specific_cache


def expand_domain_specific_reference(text: str) -> str:
    """Expand domain_specific directory reference in text.
    
    Replaces 'openchatbi/prompts/domain_specific' or 'openchatbi/prompts/domain_specific/'
    with the concatenated content of all domain-specific documentation files.
    
    Args:
        text: Text that may contain domain_specific reference
        
    Returns:
        str: Text with domain_specific reference expanded to actual content
        
    Examples:
        >>> text = "See openchatbi/prompts/domain_specific for details"
        >>> expanded = expand_domain_specific_reference(text)
        # domain_specific is replaced with actual documentation content
    """
    if not text or not isinstance(text, str):
        return text
    
    # Check if the text contains the domain_specific reference
    domain_ref_patterns = [
        "openchatbi/prompts/domain_specific/",
        "openchatbi/prompts/domain_specific"
    ]
    
    has_reference = any(pattern in text for pattern in domain_ref_patterns)
    
    if not has_reference:
        return text
    
    # Get all domain-specific documentation
    domain_docs = get_domain_specific_docs()
    
    # Define a preferred order for readability
    preferred_order = [
        "sdtm_glossary",
        "sdtm_domains",
        "dm_domain",
        "ae_domain",
        "vs_domain",
        "sdtm_examples"
    ]
    
    # Build the expanded content
    content_parts = []
    
    # Add docs in preferred order
    for doc_name in preferred_order:
        if doc_name in domain_docs:
            content_parts.append(f"\n{'='*80}\n")
            content_parts.append(f"📄 {doc_name}.md\n")
            content_parts.append(f"{'='*80}\n\n")
            content_parts.append(domain_docs[doc_name])
            content_parts.append("\n")
    
    # Add any remaining docs not in preferred order
    for doc_name, content in domain_docs.items():
        if doc_name not in preferred_order:
            content_parts.append(f"\n{'='*80}\n")
            content_parts.append(f"📄 {doc_name}.md\n")
            content_parts.append(f"{'='*80}\n\n")
            content_parts.append(content)
            content_parts.append("\n")
    
    expanded_content = "".join(content_parts)
    
    # Replace all occurrences of the domain_specific reference
    result = text
    for pattern in domain_ref_patterns:
        result = result.replace(pattern, expanded_content)
    
    return result


def expand_bi_config_domain_references(bi_config: dict) -> dict:
    """Recursively expand domain_specific references in BI config.
    
    Searches through all string values in the BI config dictionary and replaces
    any references to 'openchatbi/prompts/domain_specific' with the actual
    documentation content.
    
    Args:
        bi_config: BI configuration dictionary
        
    Returns:
        dict: BI config with domain_specific references expanded
    """
    if not isinstance(bi_config, dict):
        return bi_config
    
    expanded_config = {}
    
    for key, value in bi_config.items():
        if isinstance(value, str):
            # Expand domain_specific references in string values
            expanded_config[key] = expand_domain_specific_reference(value)
        elif isinstance(value, dict):
            # Recursively process nested dictionaries
            expanded_config[key] = expand_bi_config_domain_references(value)
        elif isinstance(value, list):
            # Process list items
            expanded_config[key] = [
                expand_domain_specific_reference(item) if isinstance(item, str)
                else expand_bi_config_domain_references(item) if isinstance(item, dict)
                else item
                for item in value
            ]
        else:
            # Keep other types as-is
            expanded_config[key] = value
    
    return expanded_config


def get_agent_prompt_template() -> str:
    """Get agent prompt template with caching."""
    global _agent_prompt_template_cache
    if _agent_prompt_template_cache is None:
        with importlib.resources.files("openchatbi.prompts").joinpath("agent_prompt.md").open("r") as f:
            prompt = f.read()

        _agent_prompt_template_cache = (
            prompt.replace("[organization]", get_organization())
            .replace("[basic_knowledge_glossary]", get_basic_knowledge())
            .replace("[extra_tool_use_rule]", get_agent_extra_tool_use_rule())
        )
    return _agent_prompt_template_cache


def get_extraction_prompt_template() -> str:
    """Get extraction prompt template with caching."""
    global _extraction_prompt_template_cache
    if _extraction_prompt_template_cache is None:
        with importlib.resources.files("openchatbi.prompts").joinpath("extraction_prompt.md").open("r") as f:
            prompt = f.read()

        _extraction_prompt_template_cache = prompt.replace("[organization]", get_organization()).replace(
            "[basic_knowledge_glossary]", get_basic_knowledge()
        )
    return _extraction_prompt_template_cache


def get_table_selection_prompt_template() -> str:
    """Get table selection prompt template with caching."""
    global _table_selection_prompt_template_cache
    if _table_selection_prompt_template_cache is None:
        with importlib.resources.files("openchatbi.prompts").joinpath("schema_linking_prompt.md").open("r") as f:
            prompt = f.read()
        _table_selection_prompt_template_cache = prompt.replace("[organization]", get_organization()).replace(
            "[basic_knowledge_glossary]", get_basic_knowledge()
        )
    return _table_selection_prompt_template_cache


def get_text2sql_prompt_template() -> str:
    """Get text2sql prompt template with caching."""
    global _text2sql_prompt_template_cache
    if _text2sql_prompt_template_cache is None:
        with importlib.resources.files("openchatbi.prompts").joinpath("text2sql_prompt.md").open("r") as f:
            prompt = f.read()
        _text2sql_prompt_template_cache = (
            prompt.replace("[organization]", get_organization())
            .replace("[basic_knowledge_glossary]", get_basic_knowledge())
            .replace("[data_warehouse_introduction]", get_data_warehouse_introduction())
        )
    return _text2sql_prompt_template_cache


def get_visualization_prompt_template() -> str:
    """Get visualization prompt template with caching."""
    global _visualization_prompt_template_cache
    if _visualization_prompt_template_cache is None:
        with importlib.resources.files("openchatbi.prompts").joinpath("visualization_prompt.md").open("r") as f:
            _visualization_prompt_template_cache = f.read()
    return _visualization_prompt_template_cache


def get_summary_prompt_template() -> str:
    """Get summary prompt template with caching."""
    global _summary_prompt_template_cache
    if _summary_prompt_template_cache is None:
        with importlib.resources.files("openchatbi.prompts").joinpath("summary_prompt.md").open("r") as f:
            _summary_prompt_template_cache = f.read()
    return _summary_prompt_template_cache


def get_text2sql_dialect_prompt_template(dialect: str) -> str:
    """Get text2sql prompt template for specific SQL dialect."""
    prompt = get_text2sql_prompt_template()
    if not prompt:
        prompt = "Generate SQL query for the given question in [dialect] dialect."

    dialect_rules = get_dialect_rules()
    prompt = prompt.replace("[dialect]", dialect).replace("[sql_dialect_rules]", dialect_rules.get(dialect, ""))
    return prompt


def reset_cache():
    """Reset all cached values. Useful for testing."""
    global _dialect_rules_cache, _domain_specific_cache, _agent_prompt_template_cache
    global _extraction_prompt_template_cache, _table_selection_prompt_template_cache
    global _text2sql_prompt_template_cache, _visualization_prompt_template_cache
    global _summary_prompt_template_cache

    _dialect_rules_cache = None
    _domain_specific_cache = None
    _agent_prompt_template_cache = None
    _extraction_prompt_template_cache = None
    _table_selection_prompt_template_cache = None
    _text2sql_prompt_template_cache = None
    _visualization_prompt_template_cache = None
    _summary_prompt_template_cache = None

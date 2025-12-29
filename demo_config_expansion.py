"""
快速演示 BI 配置中 domain_specific 引用自动扩展功能
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def demo():
    """演示自动扩展功能"""
    
    print("=" * 80)
    print("Domain Specific 引用自动扩展功能演示")
    print("=" * 80)
    
    # 演示 1: 简单文本扩展
    print("\n【演示 1】简单文本扩展")
    print("-" * 80)
    
    from openchatbi.prompts.system_prompt import expand_domain_specific_reference
    
    original = "详细信息请参考 openchatbi/prompts/domain_specific 目录"
    print(f"原始文本: {original}")
    print(f"原始长度: {len(original)} 字符")
    
    expanded = expand_domain_specific_reference(original)
    print(f"\n扩展后长度: {len(expanded)} 字符")
    print(f"包含文档: {expanded.count('📄')} 个")
    print(f"扩展比例: {len(expanded) / len(original):.0f}x")
    
    # 显示前 500 字符
    print(f"\n扩展内容预览 (前 500 字符):")
    print("-" * 80)
    print(expanded[:500])
    print("...")
    
    # 演示 2: 配置字典扩展
    print("\n\n【演示 2】配置字典扩展")
    print("-" * 80)
    
    from openchatbi.prompts.system_prompt import expand_bi_config_domain_references
    
    config = {
        "basic_knowledge_glossary": "openchatbi/prompts/domain_specific",
        "normal_field": "这是普通字段，不会被修改",
        "number_field": 123,
        "nested": {
            "info": "参考 openchatbi/prompts/domain_specific/ 了解更多"
        }
    }
    
    print("原始配置:")
    for key, value in config.items():
        if isinstance(value, str):
            print(f"  {key}: {len(value)} 字符")
        elif isinstance(value, dict):
            print(f"  {key}: [嵌套字典]")
        else:
            print(f"  {key}: {value}")
    
    expanded_config = expand_bi_config_domain_references(config)
    
    print("\n扩展后配置:")
    for key, value in expanded_config.items():
        if isinstance(value, str):
            doc_count = value.count('📄')
            print(f"  {key}: {len(value)} 字符 (包含 {doc_count} 个文档)")
        elif isinstance(value, dict):
            nested_value = list(value.values())[0]
            if isinstance(nested_value, str):
                doc_count = nested_value.count('📄')
                print(f"  {key}.info: {len(nested_value)} 字符 (包含 {doc_count} 个文档)")
        else:
            print(f"  {key}: {value}")
    
    # 演示 3: 实际 YAML 配置
    print("\n\n【演示 3】实际 YAML 配置文件")
    print("-" * 80)
    
    try:
        import yaml
        
        yaml_file = project_root / "example" / "bi_sdtm.yaml"
        
        if yaml_file.exists():
            with open(yaml_file, encoding="utf-8") as f:
                raw_config = yaml.safe_load(f)
            
            print(f"配置文件: {yaml_file.name}")
            
            if 'basic_knowledge_glossary' in raw_config:
                bkg_raw = raw_config['basic_knowledge_glossary']
                print(f"\n原始 basic_knowledge_glossary:")
                print(f"  长度: {len(bkg_raw)} 字符")
                print(f"  内容: {bkg_raw.strip()}")
                
                # 扩展配置
                expanded_config = expand_bi_config_domain_references(raw_config)
                bkg_expanded = expanded_config['basic_knowledge_glossary']
                
                print(f"\n扩展后 basic_knowledge_glossary:")
                print(f"  长度: {len(bkg_expanded)} 字符")
                print(f"  包含文档: {bkg_expanded.count('📄')} 个")
                print(f"  扩展比例: {len(bkg_expanded) / len(bkg_raw):.0f}x")
                
                # 列出包含的文档
                print(f"\n包含的文档列表:")
                for line in bkg_expanded.split('\n'):
                    if '📄' in line:
                        print(f"    {line.strip()}")
            
            print("\n✅ 配置加载和扩展成功!")
        else:
            print(f"⚠️ 配置文件不存在: {yaml_file}")
    
    except ImportError:
        print("⚠️ yaml 模块未安装，跳过此演示")
    except Exception as e:
        print(f"❌ 演示失败: {e}")
    
    # 总结
    print("\n" + "=" * 80)
    print("演示总结")
    print("=" * 80)
    print("""
✅ 核心功能:
   - 在配置文件中写入 'openchatbi/prompts/domain_specific'
   - 程序自动加载并替换为所有 domain 文档的完整内容
   - 支持嵌套字典、列表等复杂结构

📊 扩展效果:
   - 原始引用: ~35 字符
   - 扩展后: ~33,000 字符
   - 包含文档: 6 个完整的 SDTM domain 文档

💡 使用建议:
   - 简化配置文件，用引用替代大段重复内容
   - 更新 domain 文档，所有配置自动同步
   - 灵活使用，可在引用前后添加自定义说明
    """)


if __name__ == "__main__":
    try:
        demo()
        print("\n✨ 演示完成!")
    except Exception as e:
        print(f"\n❌ 演示出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

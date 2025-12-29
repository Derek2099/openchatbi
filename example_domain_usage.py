"""
演示如何使用 domain_specific 动态加载功能的简单示例
"""

# 注意：这个示例假设你已经正确安装了所有依赖
# 如果遇到导入错误，请使用 test_domain_loading.py 进行测试

def example_usage():
    """演示基本用法"""
    from openchatbi.prompts import system_prompt
    
    print("=" * 80)
    print("示例 1: 获取所有 domain 文档")
    print("=" * 80)
    
    docs = system_prompt.get_domain_specific_docs()
    print(f"找到 {len(docs)} 个文档:")
    for name in sorted(docs.keys()):
        print(f"  - {name}")
    
    print("\n" + "=" * 80)
    print("示例 2: 根据问题动态获取相关文档")
    print("=" * 80)
    
    questions = [
        "统计各治疗组的不良事件发生率",
        "分析受试者的年龄分布", 
        "血压随访视变化趋势",
    ]
    
    for q in questions:
        print(f"\n问题: {q}")
        context = system_prompt.get_domain_specific_context(q, max_domains=2)
        
        # 计算返回的文档
        doc_count = context.count("# ===== ")
        print(f"返回 {doc_count} 个相关文档，共 {len(context)} 字符")
    
    print("\n" + "=" * 80)
    print("示例 3: 获取所有文档（按优先顺序）")
    print("=" * 80)
    
    all_context = system_prompt.get_all_domain_specific_docs()
    print(f"所有文档总长度: {len(all_context)} 字符")
    print(f"文档数量: {all_context.count('# ===== ')}")

if __name__ == "__main__":
    try:
        example_usage()
        print("\n✅ 示例执行成功!")
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("\n请使用以下命令运行独立测试:")
        print("  python test_domain_loading.py")
    except Exception as e:
        print(f"❌ 执行错误: {e}")
        import traceback
        traceback.print_exc()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
排版优化功能测试
测试内容排版优化功能是否正常工作
"""

import sys
import os

# 添加当前目录到路径，以便导入模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入排版优化函数
from scripts.publish_post import optimize_content_layout, format_content

def test_layout_optimization():
    """测试排版优化功能"""
    
    print("🧪 排版优化功能测试")
    print("=" * 60)
    
    # 测试用例1：内容挤在一起的情况
    test_content1 = """🚀 AI工具年度盘点：2024年效率翻倍神器！ 🤖 AI时代已经到来，这些工具能让你工作效率提升300%！今天为大家盘点10个2024年最值得关注的AI工具，覆盖设计、写作、编程、视频全场景！ 🎨 【设计类AI工具】 1. Midjourney - AI绘画天花板，创意无限 2. DALL-E 3 - 最精准的文本转图像工具 3. Canva AI - 设计小白也能做出专业海报 📝 【写作类AI工具】 4. ChatGPT - 全能对话助手，什么问题都能答 5. Claude - 长文本处理专家，文档分析神器 6. Notion AI - 笔记整理神器，知识管理必备 💻 【编程类AI工具】 7. GitHub Copilot - 程序员的最佳搭档，代码自动补全 8. Cursor - AI驱动的代码编辑器，智能编程 🎬 【视频类AI工具】 9. Runway - 视频生成与编辑，创意视频轻松做 10. Descript - 视频剪辑像编辑文档一样简单 🌟 【使用建议】 • 新手入门：从ChatGPT和Canva开始 • 设计师必试：Midjourney让你惊艳 • 程序员首选：GitHub Copilot效率翻倍 • 视频创作者：Runway让你创意无限 💡 【小贴士】 • 大部分工具都有免费试用版 • 关注官方教程快速上手 • 结合使用效果更佳 你用过哪些AI工具？评论区分享你的体验吧！"""
    
    print("\n📝 测试用例1：内容挤在一起")
    print("-" * 40)
    print("原始内容长度:", len(test_content1))
    print("原始内容预览:", test_content1[:200])
    
    optimized1 = optimize_content_layout(test_content1)
    print("\n优化后内容长度:", len(optimized1))
    print("优化后内容预览:")
    print(optimized1[:500])
    
    # 测试用例2：格式良好的内容
    test_content2 = """🚀 AI工具年度盘点：2024年效率翻倍神器！

🤖 AI时代已经到来，这些工具能让你工作效率提升300%！今天为大家盘点10个2024年最值得关注的AI工具，覆盖设计、写作、编程、视频全场景！

🎨 【设计类AI工具】
1. Midjourney - AI绘画天花板，创意无限
2. DALL-E 3 - 最精准的文本转图像工具
3. Canva AI - 设计小白也能做出专业海报

📝 【写作类AI工具】
4. ChatGPT - 全能对话助手，什么问题都能答
5. Claude - 长文本处理专家，文档分析神器
6. Notion AI - 笔记整理神器，知识管理必备

💻 【编程类AI工具】
7. GitHub Copilot - 程序员的最佳搭档，代码自动补全
8. Cursor - AI驱动的代码编辑器，智能编程

🎬 【视频类AI工具】
9. Runway - 视频生成与编辑，创意视频轻松做
10. Descript - 视频剪辑像编辑文档一样简单

🌟 【使用建议】
• 新手入门：从ChatGPT和Canva开始
• 设计师必试：Midjourney让你惊艳
• 程序员首选：GitHub Copilot效率翻倍
• 视频创作者：Runway让你创意无限

💡 【小贴士】
• 大部分工具都有免费试用版
• 关注官方教程快速上手
• 结合使用效果更佳

你用过哪些AI工具？评论区分享你的体验吧！"""
    
    print("\n\n📝 测试用例2：格式良好的内容")
    print("-" * 40)
    print("原始内容长度:", len(test_content2))
    
    optimized2 = optimize_content_layout(test_content2)
    print("优化后内容长度:", len(optimized2))
    
    # 检查是否保持原有格式
    if test_content2 == optimized2:
        print("✅ 格式良好的内容保持不变")
    else:
        print("⚠️  格式良好的内容被修改")
        print("差异长度:", len(optimized2) - len(test_content2))
    
    # 测试用例3：格式化内容（包含标签）
    print("\n\n📝 测试用例3：完整格式化（标题+内容+标签）")
    print("-" * 40)
    
    title = "🚀 AI工具年度盘点：2024年效率翻倍神器"
    content = test_content2
    tags = ["AI工具", "人工智能", "效率工具", "ChatGPT", "Midjourney", "GitHubCopilot", "Runway", "设计工具", "编程工具", "视频剪辑", "效率提升", "科技前沿", "数字生活"]
    
    formatted = format_content(title, content, tags)
    print("格式化后总长度:", len(formatted))
    print("格式化后内容预览（最后200字符）:")
    print(formatted[-200:])
    
    # 检查字数限制
    if len(formatted) <= 1000:
        print("✅ 字数符合限制（≤1000）")
    else:
        print("❌ 字数超限")
    
    # 检查排版质量
    print("\n\n🎯 排版质量检查")
    print("-" * 40)
    
    # 检查换行数量
    newline_count = formatted.count('\n')
    print(f"换行符数量: {newline_count}")
    
    # 检查段落间距
    double_newline_count = formatted.count('\n\n')
    print(f"段落间距数量: {double_newline_count}")
    
    # 检查标签格式
    if formatted.endswith('#'):
        print("✅ 标签格式正确")
    else:
        # 查找标签位置
        last_newline = formatted.rfind('\n')
        if last_newline != -1:
            tags_section = formatted[last_newline:].strip()
            if tags_section.startswith('#'):
                print("✅ 标签格式正确")
            else:
                print("⚠️  标签格式可能有问题")
    
    print("\n" + "=" * 60)
    print("✅ 排版优化功能测试完成")
    
    return 0

def main():
    """主函数"""
    try:
        return test_layout_optimization()
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
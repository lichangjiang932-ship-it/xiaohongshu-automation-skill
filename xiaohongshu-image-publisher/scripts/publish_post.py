#!/usr/bin/env python3
"""
小红书帖子发布脚本
自动化填写内容和发布帖子
"""

import os
import sys
import json
import argparse
from datetime import datetime

def check_content_limits(title, content):
    """
    检查内容字数限制
    """
    # 小红书限制
    MAX_TITLE_LENGTH = 20  # 字符数
    MAX_CONTENT_LENGTH = 1000  # 字符数
    
    title_length = len(title)
    content_length = len(content)
    
    print(f"📝 字数检查:")
    print(f"  标题: {title_length}/{MAX_TITLE_LENGTH} 字符")
    print(f"  正文: {content_length}/{MAX_CONTENT_LENGTH} 字符")
    
    issues = []
    
    if title_length > MAX_TITLE_LENGTH:
        issues.append(f"标题超限 ({title_length} > {MAX_TITLE_LENGTH})")
    
    if content_length > MAX_CONTENT_LENGTH:
        issues.append(f"正文超限 ({content_length} > {MAX_CONTENT_LENGTH})")
    
    if issues:
        print("❌ 字数检查失败:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    
    print("✅ 字数检查通过")
    return True

def format_content(title, content, tags):
    """
    格式化内容
    """
    # 确保标签格式正确
    formatted_tags = []
    for tag in tags:
        if not tag.startswith("#"):
            tag = "#" + tag
        formatted_tags.append(tag)
    
    # 优化排版：确保换行和段落间距
    # 处理内容中的换行
    content_lines = content.split('\n')
    formatted_lines = []
    
    for line in content_lines:
        line = line.strip()
        if line:
            formatted_lines.append(line)
    
    # 用空行连接段落，增强可读性
    formatted_content = '\n\n'.join(formatted_lines)
    
    # 构建完整内容
    full_content = f"{title}\n\n{formatted_content}"
    
    if formatted_tags:
        # 在正文和标签之间添加2个空行
        full_content += "\n\n" + " ".join(formatted_tags)
    
    return full_content

def optimize_content_layout(content):
    """
    优化内容排版
    确保段落清晰、间距合适、可读性好
    """
    # 常见排版问题修复
    optimizations = [
        # 修复连续多个换行
        (r'\n{3,}', '\n\n'),
        # 修复段落开头空格
        (r'^\s+', ''),
        # 修复段落结尾空格
        (r'\s+$', ''),
        # 确保标题后有换行
        (r'([!?。！？])\s*', r'\1\n'),
        # 确保列表项有换行
        (r'(\d+\.\s)', r'\n\1'),
        # 确保分类标题后有换行
        (r'(【.+】)', r'\n\1\n'),
    ]
    
    import re
    optimized = content
    
    for pattern, replacement in optimizations:
        optimized = re.sub(pattern, replacement, optimized, flags=re.MULTILINE)
    
    # 确保总字数不超过1000
    if len(optimized) > 1000:
        optimized = optimized[:1000]
    
    return optimized

def generate_browser_commands(title, content, tags):
    """
    生成浏览器自动化命令
    """
    commands = []
    
    # 1. 导航到发布页面
    commands.append({
        "action": "navigate",
        "url": "https://creator.xiaohongshu.com/publish/publish?tab=image"
    })
    
    # 2. 等待页面加载
    commands.append({
        "action": "wait",
        "timeMs": 2000
    })
    
    # 3. 点击标题输入框并输入标题
    commands.append({
        "action": "click",
        "ref": "e212"  # 标题输入框ref
    })
    
    commands.append({
        "action": "type",
        "ref": "e212",
        "text": title
    })
    
    # 4. 点击正文输入框并输入内容
    commands.append({
        "action": "click",
        "ref": "e221"  # 正文输入框ref
    })
    
    # 输入正文（分段落）
    content_lines = content.split('\n')
    for line in content_lines:
        if line.strip():
            commands.append({
                "action": "type",
                "ref": "e221",
                "text": line + "\n"
            })
    
    # 5. 添加标签（使用JavaScript一次性设置，避免内容被删除）
    if tags:
        # 重要经验教训：使用type命令添加标签会清空正文内容
        # 解决方案：使用JavaScript一次性设置完整内容
        tags_text = "\\n\\n" + " ".join(tags)
        js_code = f'''
        () => {{
          // 找到内容输入框
          const contentInput = document.querySelector('textarea, [contenteditable="true"]');
          if (!contentInput) return false;
          
          // 获取当前内容
          let currentContent = '';
          if (contentInput.tagName === 'TEXTAREA') {{
            currentContent = contentInput.value;
          }} else {{
            currentContent = contentInput.textContent;
          }}
          
          // 在末尾添加标签
          const newContent = currentContent + `{tags_text}`;
          
          // 设置新内容
          if (contentInput.tagName === 'TEXTAREA') {{
            contentInput.value = newContent;
          }} else {{
            contentInput.textContent = newContent;
          }}
          
          // 触发事件
          contentInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
          contentInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
          
          return true;
        }}
        '''
        
        commands.append({
            "action": "evaluate",
            "fn": js_code
        })
        
        # 经验教训：之前使用type命令添加标签时，小红书页面会清空正文内容
        # 必须使用JavaScript直接设置value属性
    
    # 6. 点击发布按钮
    commands.append({
        "action": "click",
        "ref": "e516"  # 发布按钮ref
    })
    
    # 7. 等待发布完成
    commands.append({
        "action": "wait",
        "timeMs": 3000
    })
    
    return commands

def save_workflow(title, content, tags, commands, output_dir="./workflows"):
    """
    保存工作流配置
    """
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    workflow_file = os.path.join(output_dir, f"workflow_{timestamp}.json")
    
    workflow = {
        "metadata": {
            "created_at": datetime.now().isoformat(),
            "platform": "xiaohongshu",
            "version": "1.0.0"
        },
        "content": {
            "title": title,
            "content": content,
            "tags": tags,
            "title_length": len(title),
            "content_length": len(content),
            "tags_count": len(tags)
        },
        "automation": {
            "commands": commands,
            "total_steps": len(commands)
        }
    }
    
    with open(workflow_file, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, ensure_ascii=False, indent=2)
    
    print(f"📁 工作流已保存: {workflow_file}")
    return workflow_file

def create_execution_script(commands, output_file="./execute_publish.sh"):
    """
    创建执行脚本
    """
    script_content = """#!/bin/bash

# 小红书自动化发布脚本
# 生成时间: {timestamp}

echo "🚀 开始小红书自动化发布..."

# 步骤计数器
step=1
total_steps={total_steps}

"""

    # 添加每个命令
    for cmd in commands:
        action = cmd.get("action", "")
        
        if action == "navigate":
            script_content += f"""
echo "[$step/$total_steps] 导航到发布页面..."
openclaw browser act --profile openclaw --action navigate --url "{cmd['url']}"
sleep 2
"""
        
        elif action == "wait":
            script_content += f"""
echo "[$step/$total_steps] 等待页面加载..."
sleep {cmd['timeMs'] // 1000}
"""
        
        elif action == "click":
            script_content += f"""
echo "[$step/$total_steps] 点击元素..."
openclaw browser act --profile openclaw --action click --ref "{cmd['ref']}"
sleep 1
"""
        
        elif action == "type":
            # 转义文本中的特殊字符
            text = cmd['text'].replace('"', '\\"').replace('$', '\\$')
            script_content += f"""
echo "[$step/$total_steps] 输入文本..."
openclaw browser act --profile openclaw --action type --ref "{cmd['ref']}" --text "{text}"
sleep 0.5
"""
        
        elif action == "press":
            script_content += f"""
echo "[$step/$total_steps] 按键操作..."
openclaw browser act --profile openclaw --action press --ref "{cmd['ref']}" --key "{cmd['key']}"
sleep 0.5
"""
        
        step += 1
    
    script_content += """
echo "🎉 发布流程执行完成！"
echo "请检查小红书账号确认发布是否成功。"
"""
    
    # 替换变量
    script_content = script_content.format(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total_steps=len(commands)
    )
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    # 添加执行权限
    os.chmod(output_file, 0o755)
    
    print(f"📝 执行脚本已创建: {output_file}")
    return output_file

def main():
    parser = argparse.ArgumentParser(description="小红书帖子发布脚本")
    parser.add_argument("--title", required=True, help="帖子标题")
    parser.add_argument("--content", required=True, help="帖子正文")
    parser.add_argument("--tags", nargs="+", default=[], help="标签列表")
    parser.add_argument("--content-file", help="从文件读取正文内容")
    parser.add_argument("--tags-file", help="从文件读取标签")
    parser.add_argument("--output-dir", default="./workflows", help="工作流输出目录")
    parser.add_argument("--generate-script", action="store_true", help="生成执行脚本")
    
    args = parser.parse_args()
    
    # 从文件读取内容
    if args.content_file and os.path.exists(args.content_file):
        with open(args.content_file, 'r', encoding='utf-8') as f:
            args.content = f.read().strip()
    
    # 从文件读取标签
    if args.tags_file and os.path.exists(args.tags_file):
        with open(args.tags_file, 'r', encoding='utf-8') as f:
            args.tags = [line.strip() for line in f if line.strip()]
    
    print("🚀 小红书帖子发布工具")
    print("=" * 60)
    
    # 优化内容排版
    print("\n🎨 优化内容排版...")
    original_length = len(args.content)
    args.content = optimize_content_layout(args.content)
    optimized_length = len(args.content)
    
    if original_length != optimized_length:
        print(f"  原始长度: {original_length} 字符")
        print(f"  优化后长度: {optimized_length} 字符")
        print(f"  变化: {optimized_length - original_length} 字符")
    
    # 检查字数限制
    if not check_content_limits(args.title, args.content):
        return 1
    
    # 格式化内容
    full_content = format_content(args.title, args.content, args.tags)
    
    print(f"\n📋 内容摘要:")
    print(f"  标题: {args.title}")
    print(f"  正文长度: {len(args.content)} 字符")
    print(f"  标签数量: {len(args.tags)} 个")
    if args.tags:
        print(f"  标签: {' '.join(args.tags)}")
    
    # 生成自动化命令
    print("\n🔧 生成自动化命令...")
    commands = generate_browser_commands(args.title, args.content, args.tags)
    print(f"✅ 生成 {len(commands)} 个自动化步骤")
    
    # 保存工作流
    workflow_file = save_workflow(args.title, args.content, args.tags, commands, args.output_dir)
    
    # 生成执行脚本
    if args.generate_script:
        script_file = create_execution_script(commands)
        print(f"\n📜 执行脚本: {script_file}")
        print(f"  运行命令: ./{os.path.basename(script_file)}")
    
    print("\n" + "=" * 60)
    print("✅ 发布准备完成！")
    print("=" * 60)
    
    print("\n📝 下一步:")
    print("1. 确保图片已上传到小红书")
    print("2. 运行自动化命令或执行脚本")
    print("3. 检查小红书账号确认发布成功")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
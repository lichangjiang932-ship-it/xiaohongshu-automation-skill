# 小红书图片发布自动化示例工作流

## 示例：发布"AI工具年度盘点"帖子

### 1. 准备工作
```bash
# 进入技能目录
cd skills/xiaohongshu-image-publisher

# 创建示例工作目录
mkdir -p example_workflow
cd example_workflow
```

### 2. 准备内容
```bash
# 创建标题和正文
cat > content.txt << 'EOF'
🚀 AI工具年度盘点：2024年效率翻倍神器！

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

你用过哪些AI工具？评论区分享你的体验吧！
EOF

# 创建标签文件
cat > tags.txt << 'EOF'
AI工具
人工智能
效率工具
ChatGPT
Midjourney
GitHubCopilot
Runway
设计工具
编程工具
视频剪辑
效率提升
科技前沿
数字生活
EOF
```

### 3. 生成图片
```bash
# 生成5张AI工具主题图片
../scripts/create_images.sh --theme "AI工具" --count 5 --output-dir ./generated_images
```

输出：
```
🎨 开始生成小红书图片...
主题: AI工具
数量: 5
输出目录: ./generated_images
尺寸: 1920x1920

生成封面图片...
生成图片 2/5...
生成图片 3/5...
生成图片 4/5...
生成图片 5/5...

🎉 图片生成完成！
📁 输出目录: ./generated_images

📋 生成的图片:
  - 01_cover.jpg (45.2KB)
  - 02_content_1.jpg (52.7KB)
  - 03_content_2.jpg (59.0KB)
  - 04_content_3.jpg (49.5KB)
  - 05_content_4.jpg (50.0KB)
```

### 4. 准备图片上传
```bash
# 准备图片上传
python ../scripts/upload_images.py --images-dir ./generated_images
```

输出：
```
🚀 小红书图片上传准备工具
==================================================
📁 上传目录已创建: /tmp/openclaw/uploads
📂 扫描目录: ./generated_images
📊 准备上传 5 张图片
✅ 已复制: 01_cover.jpg (0.0MB)
✅ 已复制: 02_content_1.jpg (0.1MB)
✅ 已复制: 03_content_2.jpg (0.1MB)
✅ 已复制: 04_content_3.jpg (0.0MB)
✅ 已复制: 05_content_4.jpg (0.0MB)
🎉 准备完成！5 张图片已就绪

==================================================
📋 上传准备完成
==================================================

📁 上传目录内容:
  - 01_cover.jpg (45.2KB)
  - 02_content_1.jpg (52.7KB)
  - 03_content_2.jpg (59.0KB)
  - 04_content_3.jpg (49.5KB)
  - 05_content_4.jpg (50.0KB)

📝 上传命令:
# 使用OpenClaw browser工具上传图片
browser upload \
  --profile openclaw \
  --targetId "YOUR_TARGET_ID" \
  --paths ["/tmp/openclaw/uploads/01_cover.jpg", "/tmp/openclaw/uploads/02_content_1.jpg", "/tmp/openclaw/uploads/03_content_2.jpg", "/tmp/openclaw/uploads/04_content_3.jpg", "/tmp/openclaw/uploads/05_content_4.jpg"]

✅ 准备完成！现在可以使用 browser upload 工具上传图片了。
```

### 5. 上传图片（手动执行）
```bash
# 在实际环境中，需要先打开小红书页面
# 然后执行上传命令（需要替换YOUR_TARGET_ID）
openclaw browser upload \
  --profile openclaw \
  --targetId "D16BC54CB29DE4E3A3C4EDED04360448" \
  --paths '["/tmp/openclaw/uploads/01_cover.jpg", "/tmp/openclaw/uploads/02_content_1.jpg", "/tmp/openclaw/uploads/03_content_2.jpg", "/tmp/openclaw/uploads/04_content_3.jpg", "/tmp/openclaw/uploads/05_content_4.jpg"]'
```

### 6. 准备发布
```bash
# 生成发布工作流
python ../scripts/publish_post.py \
  --title "🚀 AI工具年度盘点：2024年效率翻倍神器" \
  --content-file content.txt \
  --tags-file tags.txt \
  --generate-script
```

输出：
```
🚀 小红书帖子发布工具
============================================================
📝 字数检查:
  标题: 14/20 字符
  正文: 564/1000 字符
✅ 字数检查通过

📋 内容摘要:
  标题: 🚀 AI工具年度盘点：2024年效率翻倍神器
  正文长度: 564 字符
  标签数量: 13 个
  标签: #AI工具 #人工智能 #效率工具 #ChatGPT #Midjourney #GitHubCopilot #Runway #设计工具 #编程工具 #视频剪辑 #效率提升 #科技前沿 #数字生活

🔧 生成自动化命令...
✅ 生成 11 个自动化步骤
📁 工作流已保存: ./workflows/workflow_20260227_145732.json
📝 执行脚本已创建: ./execute_publish.sh

============================================================
✅ 发布准备完成！
============================================================

📝 下一步:
1. 确保图片已上传到小红书
2. 运行自动化命令或执行脚本
3. 检查小红书账号确认发布成功
```

### 7. 执行发布
```bash
# 运行发布脚本
./execute_publish.sh
```

脚本内容示例：
```bash
#!/bin/bash

# 小红书自动化发布脚本
# 生成时间: 2026-02-27 14:57:32

echo "🚀 开始小红书自动化发布..."

# 步骤计数器
step=1
total_steps=11

echo "[1/11] 导航到发布页面..."
openclaw browser act --profile openclaw --action navigate --url "https://creator.xiaohongshu.com/publish/publish?tab=image"
sleep 2

echo "[2/11] 等待页面加载..."
sleep 2

echo "[3/11] 点击元素..."
openclaw browser act --profile openclaw --action click --ref "e212"
sleep 1

echo "[4/11] 输入文本..."
openclaw browser act --profile openclaw --action type --ref "e212" --text "🚀 AI工具年度盘点：2024年效率翻倍神器"
sleep 0.5

# ... 更多步骤 ...

echo "🎉 发布流程执行完成！"
echo "请检查小红书账号确认发布是否成功。"
```

### 8. 验证发布
1. 打开小红书App或网页版
2. 检查个人主页
3. 确认新帖子"AI工具年度盘点"已发布
4. 检查图片、标题、正文、标签是否正确

## 故障排除

### 常见问题1：图片上传失败
**症状**：`browser upload`返回错误
**解决方案**：
```bash
# 检查上传目录
ls -la /tmp/openclaw/uploads/

# 检查文件权限
chmod 644 /tmp/openclaw/uploads/*.jpg

# 重新上传单张图片测试
openclaw browser upload --profile openclaw --paths '["/tmp/openclaw/uploads/01_cover.jpg"]'
```

### 常见问题2：页面元素找不到
**症状**：自动化命令失败，提示元素不存在
**解决方案**：
```bash
# 获取当前页面快照
openclaw browser snapshot --profile openclaw --refs aria

# 更新脚本中的ref值
# 修改publish_post.py中的ref值
```

### 常见问题3：发布后页面不刷新
**症状**：点击发布后页面没有变化
**解决方案**：
```bash
# 手动刷新页面
openclaw browser act --profile openclaw --action evaluate --fn "() => location.reload()"

# 检查是否发布成功
openclaw browser snapshot --profile openclaw
```

### 常见问题4：添加标签时内容被删除
**症状**：发布后帖子有标题和标签，但没有正文内容
**原因**：在正文输入框添加标签时，可能不小心覆盖或删除了正文
**解决方案**：
```python
# 正确的操作顺序：
# 1. 先输入完整正文
browser_commands.append({
    "action": "type",
    "ref": "e166",  # 正文输入框ref
    "text": "完整正文内容..."
})

# 2. 将光标移动到正文末尾
browser_commands.append({
    "action": "press", 
    "ref": "e166",
    "key": "End"
})

# 3. 等待确保光标位置正确
browser_commands.append({
    "action": "wait",
    "timeMs": 500
})

# 4. 在末尾添加标签
browser_commands.append({
    "action": "type",
    "ref": "e166",
    "text": "\n\n#标签1 #标签2"
})

# 经验教训：这是实际遇到并解决的问题
# 确保内容完整性的关键步骤

## 自动化优化建议

### 1. 添加重试机制
```python
# 在脚本中添加重试逻辑
import time

def retry_operation(operation, max_retries=3, delay=2):
    for attempt in range(max_retries):
        try:
            return operation()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"重试 {attempt + 1}/{max_retries}: {e}")
            time.sleep(delay)
```

### 2. 添加日志记录
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('xiaohongshu_publish.log'),
        logging.StreamHandler()
    ]
)
```

### 3. 添加状态检查
```python
def check_publish_status():
    """检查发布状态"""
    # 检查页面是否回到上传界面
    # 检查是否有成功提示
    # 记录发布结果
    pass
```

## 扩展功能

### 1. 批量发布
```bash
# 创建多个内容文件
for theme in "AI工具" "旅行攻略" "美食分享"; do
  ./scripts/create_images.sh --theme "$theme" --count 5
  python scripts/publish_post.py --title "$theme分享" --content-file "${theme}.txt"
done
```

### 2. 定时发布
```bash
# 使用cron定时发布
0 12 * * * cd /path/to/skills/xiaohongshu-image-publisher && ./execute_publish.sh
```

### 3. 数据统计
```python
# 记录发布数据
import sqlite3

def record_publish_data(title, image_count, publish_time, status):
    """记录发布数据"""
    conn = sqlite3.connect('publish_stats.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO publishes (title, image_count, publish_time, status)
        VALUES (?, ?, ?, ?)
    ''', (title, image_count, publish_time, status))
    conn.commit()
    conn.close()
```

## 总结

这个示例工作流展示了完整的自动化发布流程：
1. ✅ 内容准备
2. ✅ 图片生成  
3. ✅ 图片上传准备
4. ✅ 发布工作流生成
5. ✅ 自动化执行

通过这个技能，你可以快速、高效地发布高质量的小红书内容，节省大量手动操作时间。
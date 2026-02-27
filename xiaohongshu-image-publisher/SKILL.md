# 小红书图片发布自动化技能

## 概述
自动化发布带图片的小红书帖子，包括图片生成、上传、内容填写和发布的全流程。

## 适用场景
- 需要发布带多张图片的小红书笔记
- 需要自动化图片上传和内容填写
- 需要批量发布小红书内容
- 需要将文字内容自动转换为图文帖子

## 前置条件
1. **小红书账号**：已登录小红书创作中心
2. **图片素材**：需要发布的图片文件（JPG/PNG格式）
3. **内容准备**：标题、正文、标签
4. **系统要求**：OpenClaw浏览器工具可用

## 技能文件结构
```
skills/xiaohongshu-image-publisher/
├── SKILL.md                  # 本技能文档
├── scripts/
│   ├── create_images.sh      # 图片生成脚本
│   ├── upload_images.py      # 图片上传脚本
│   └── publish_post.py       # 发布脚本
├── templates/
│   ├── image_template.md     # 图片生成模板
│   └── content_template.md   # 内容模板
└── examples/
    └── example_workflow.md   # 示例工作流
```

## 核心功能

### 1. 图片生成
```bash
# 生成1920x1920的图片
./scripts/create_images.sh --theme "AI工具" --count 5 --output-dir ./images
```

### 2. 图片上传
```python
# 自动化上传图片到小红书
python scripts/upload_images.py \
  --images-dir ./images \
  --upload-dir /tmp/openclaw/uploads
```

### 3. 内容发布
```python
# 自动化发布帖子
python scripts/publish_post.py \
  --title "AI工具年度盘点" \
  --content "正文内容..." \
  --tags "#AI工具 #人工智能"
```

## 详细步骤

### 步骤1：准备图片
1. 图片格式：JPG或PNG
2. 推荐尺寸：1920x1920像素
3. 图片数量：3-9张（小红书限制）
4. 文件大小：≤32MB

### 步骤2：上传图片
1. 将图片复制到上传目录：`/tmp/openclaw/uploads/`
2. 使用`browser upload`功能上传
3. 处理页面导航问题

### 步骤3：填写内容
1. 标题：≤20个字符（包括表情符号）
2. 正文：≤1000个字符
3. 标签：12-15个相关标签

### 步骤4：发布帖子
1. 点击发布按钮
2. 验证发布成功

## 自动化脚本

### 图片生成脚本 (`scripts/create_images.sh`)
```bash
#!/bin/bash
# 创建小红书规格的图片
# 参数：--theme 主题 --count 数量 --output-dir 输出目录
```

### 图片上传脚本 (`scripts/upload_images.py`)
```python
#!/usr/bin/env python3
# 自动化上传图片到小红书
# 功能：复制图片到上传目录，使用browser upload功能
```

### 发布脚本 (`scripts/publish_post.py`)
```python
#!/usr/bin/env python3
# 自动化发布小红书帖子
# 功能：填写标题、正文、标签，点击发布
```

## 常见问题解决

### 问题1：页面导航失败
**症状**：无法进入图片上传界面
**解决方案**：
```javascript
// 使用JavaScript强制导航
window.location.href = 'https://creator.xiaohongshu.com/publish/publish?tab=image&t=' + Date.now();
```

### 问题2：图片上传失败
**症状**：`browser upload`返回错误
**解决方案**：
1. 确保图片在`/tmp/openclaw/uploads/`目录
2. 检查文件权限
3. 使用绝对路径

### 问题3：内容字数超限
**症状**：发布失败，提示字数超限
**解决方案**：
1. 标题：≤20字符
2. 正文：≤1000字符
3. 使用`wc -m`命令检查字数

### 问题4：添加标签时内容被删除
**症状**：在正文末尾添加标签时，不小心覆盖或删除了正文内容
**根本原因**：小红书页面在使用`type`命令添加标签时，可能会清空或覆盖正文内容
**解决方案**：
1. **使用JavaScript一次性设置**：将正文和标签一起设置，避免分步操作
   ```javascript
   // 正确的做法：一次性设置完整内容
   const fullContent = `完整正文内容...\n\n#标签1 #标签2`;
   
   // 找到内容输入框
   const contentInput = document.querySelector('textarea, [contenteditable="true"]');
   if (contentInput.tagName === 'TEXTAREA') {
     contentInput.value = fullContent;
   } else {
     contentInput.textContent = fullContent;
   }
   
   // 触发输入事件
   contentInput.dispatchEvent(new Event('input', { bubbles: true }));
   contentInput.dispatchEvent(new Event('change', { bubbles: true }));
   ```

2. **避免使用type命令添加标签**：`type`命令可能会触发页面的清空逻辑

3. **内容验证**：发布前检查页面快照，确保内容完整

**经验教训**：这是实际遇到并解决的问题。使用`browser act --action type`添加标签时，小红书页面会清空正文内容。必须使用JavaScript直接设置`value`属性。

### 问题5：正文排版不美观
**症状**：发布后的帖子内容挤在一起，没有换行和段落间距，可读性差
**根本原因**：
1. 小红书页面可能将换行符`\\n`转换为空格
2. JavaScript设置内容时格式丢失
3. 内容输入框可能不支持多行文本格式

**解决方案**：
1. **使用正确的换行符**：确保使用`\\n`而不是其他换行方式
2. **分段设置内容**：如果一次性设置失败，尝试分段设置
3. **使用type命令分段输入**：对于长内容，可以分段使用type命令
4. **添加空行分隔**：在不同部分之间添加空行

**优化后的内容结构示例**：
```javascript
const content = `🚀 AI工具年度盘点：2024年效率翻倍神器！

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

#AI工具 #人工智能 #效率工具 #ChatGPT #Midjourney #GitHubCopilot #Runway #设计工具 #编程工具 #视频剪辑 #效率提升 #科技前沿 #数字生活`;
```

**排版优化技巧**：
1. **标题与正文之间**：添加1-2个空行
2. **不同分类之间**：添加1个空行
3. **列表项**：使用换行分隔
4. **标签部分**：在正文和标签之间添加2个空行
5. **使用emoji和符号**：增强视觉层次感

**实际案例**：2026-02-27发布的"AI工具年度盘点"帖子，虽然内容完整，但排版不美观。通过优化排版结构，可以显著提升阅读体验。

## 最佳实践

### 图片优化
1. **尺寸**：1920x1920像素
2. **格式**：JPG（压缩质量85%）
3. **命名**：按顺序命名（01_cover.jpg, 02_content.jpg...）
4. **内容**：每张图片有明确的主题

### 内容优化
1. **标题**：7-15个字符最佳，包含表情符号
2. **正文**：800-900字符为宜，分段清晰
3. **标签**：12-15个相关标签，按热度排序
4. **结构**：使用emoji和分段提高可读性

### 自动化优化
1. **错误处理**：添加重试机制
2. **日志记录**：记录每个步骤的状态
3. **状态检查**：发布后验证是否成功
4. **资源清理**：清理临时文件

## 示例工作流

### 完整自动化发布
```bash
# 1. 生成图片
./scripts/create_images.sh --theme "旅行攻略" --count 5

# 2. 上传图片
python scripts/upload_images.py --images-dir ./generated_images

# 3. 发布帖子
python scripts/publish_post.py \
  --title "云南旅行全攻略" \
  --content "正文内容..." \
  --tags "#旅行 #云南 #攻略"
```

### 快速发布现有图片
```bash
# 直接上传并发布
python scripts/upload_images.py --images ./pic1.jpg ./pic2.jpg ./pic3.jpg
python scripts/publish_post.py --title "今日分享" --content "分享美好生活"
```

## 技术要点

### 1. 浏览器自动化
- 使用OpenClaw browser工具
- 支持文件上传功能
- 处理页面交互

### 2. 文件处理
- 图片格式转换
- 尺寸调整
- 批量处理

### 3. 内容管理
- 字数统计
- 标签优化
- 内容模板

## 注意事项

### 安全考虑
1. **账号安全**：不要硬编码账号信息
2. **内容审核**：确保内容符合平台规则
3. **频率限制**：避免频繁发布触发限制

### 平台限制
1. **字数限制**：标题≤20字，正文≤1000字
2. **图片限制**：3-9张，≤32MB
3. **标签限制**：最多20个标签

### 性能优化
1. **图片压缩**：减少上传时间
2. **批量处理**：一次处理多张图片
3. **缓存利用**：减少重复操作

## 更新日志

### v1.0.0 (2026-02-27)
- 初始版本发布
- 支持图片生成、上传、发布全流程
- 包含错误处理和优化建议

## 相关技能
- [小红书纯文本发布](../xiaohongshu/) - 纯文本发布技能
- [FFmpeg多媒体处理](../ffmpeg/) - 图片和视频处理
- [内容创作助手](../content-creator/) - 内容生成和优化

---

**使用提示**：首次使用前，建议先在小号测试完整流程，确保自动化脚本正常工作。
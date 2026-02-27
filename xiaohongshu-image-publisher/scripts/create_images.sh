#!/bin/bash

# 小红书图片生成脚本
# 生成符合小红书规格的图片（1920x1920）

set -e

# 默认参数
THEME="AI工具"
COUNT=5
OUTPUT_DIR="./generated_images"
WIDTH=1920
HEIGHT=1920

# 颜色方案
COLORS=(
    "0x1a1a2e"  # 深蓝
    "0x533483"  # 紫色
    "0x00b4d8"  # 亮蓝
    "0x2a9d8f"  # 绿色
    "0x9d4edd"  # 深紫
    "0xff6b6b"  # 红色
    "0xffd166"  # 黄色
    "0x06d6a0"  # 青色
    "0x118ab2"  # 蓝色
)

# 图标
ICONS=("🚀" "🎨" "📝" "💻" "🎬" "📱" "🎯" "💡" "🌟")

# 显示帮助信息
show_help() {
    echo "小红书图片生成脚本"
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -t, --theme TEXT     图片主题（默认: AI工具）"
    echo "  -c, --count NUM      生成图片数量（默认: 5）"
    echo "  -o, --output-dir DIR 输出目录（默认: ./generated_images）"
    echo "  -h, --help           显示帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 --theme \"旅行攻略\" --count 3"
    echo "  $0 -t \"美食分享\" -c 4 -o ./food_images"
}

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--theme)
            THEME="$2"
            shift 2
            ;;
        -c|--count)
            COUNT="$2"
            shift 2
            ;;
        -o|--output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "错误: 未知参数 $1"
            show_help
            exit 1
            ;;
    esac
done

# 检查FFmpeg是否安装
if ! command -v ffmpeg &> /dev/null; then
    echo "错误: FFmpeg未安装"
    echo "请安装FFmpeg: brew install ffmpeg 或 apt-get install ffmpeg"
    exit 1
fi

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

echo "🎨 开始生成小红书图片..."
echo "主题: $THEME"
echo "数量: $COUNT"
echo "输出目录: $OUTPUT_DIR"
echo "尺寸: ${WIDTH}x${HEIGHT}"
echo ""

# 生成封面图片
echo "生成封面图片..."
ffmpeg -f lavfi -i "color=c=${COLORS[0]}:s=${WIDTH}x${HEIGHT}:d=1" \
    -vf "drawtext=text='${ICONS[0]}':fontcolor=white:fontsize=200:x=(w-text_w)/2:y=300,\
         drawtext=text='${THEME}':fontcolor=white:fontsize=120:x=(w-text_w)/2:y=550,\
         drawtext=text='小红书内容分享':fontcolor=#cccccc:fontsize=80:x=(w-text_w)/2:y=750,\
         drawtext=text='优质内容值得收藏':fontcolor=#aaaaaa:fontsize=60:x=(w-text_w)/2:y=900,\
         drawbox=x=100:y=1000:w=$((WIDTH-200)):h=5:color=white@0.3,\
         drawtext=text='小红书 @创作者':fontcolor=#888888:fontsize=40:x=100:y=$((HEIGHT-100))" \
    -frames:v 1 -y "$OUTPUT_DIR/01_cover.jpg" 2>/dev/null

# 生成内容图片
for ((i=1; i<COUNT; i++)); do
    img_num=$((i+1))
    filename=$(printf "%02d_content_%d.jpg" "$img_num" "$i")
    
    color_idx=$((i % ${#COLORS[@]}))
    icon_idx=$((i % ${#ICONS[@]}))
    
    echo "生成图片 $img_num/$COUNT..."
    
    ffmpeg -f lavfi -i "color=c=${COLORS[color_idx]}:s=${WIDTH}x${HEIGHT}:d=1" \
        -vf "drawtext=text='${ICONS[icon_idx]}':fontcolor=white:fontsize=200:x=(w-text_w)/2:y=300,\
             drawtext=text='${THEME}':fontcolor=white:fontsize=120:x=(w-text_w)/2:y=550,\
             drawtext=text='第${img_num}部分':fontcolor=#cccccc:fontsize=80:x=(w-text_w)/2:y=750,\
             drawtext=text='精彩内容持续更新':fontcolor=#aaaaaa:fontsize=60:x=(w-text_w)/2:y=900,\
             drawbox=x=100:y=1000:w=$((WIDTH-200)):h=5:color=white@0.3,\
             drawtext=text='关注获取更多内容':fontcolor=#dddddd:fontsize=50:x=(w-text_w)/2:y=1200,\
             drawtext=text='小红书 @创作者':fontcolor=#888888:fontsize=40:x=100:y=$((HEIGHT-100))" \
        -frames:v 1 -y "$OUTPUT_DIR/$filename" 2>/dev/null
done

echo ""
echo "🎉 图片生成完成！"
echo "📁 输出目录: $OUTPUT_DIR"
echo ""
echo "📋 生成的图片:"
ls -la "$OUTPUT_DIR"/*.jpg | while read -r file; do
    filename=$(basename "$file")
    size=$(wc -c < "$file" | awk '{printf "%.1f", $1/1024}')
    echo "  - $filename (${size}KB)"
done

echo ""
echo "✅ 所有图片已生成完成，可以用于小红书发布。"
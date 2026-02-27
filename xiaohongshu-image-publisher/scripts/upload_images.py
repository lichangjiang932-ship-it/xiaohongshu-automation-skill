#!/usr/bin/env python3
"""
小红书图片上传脚本
自动化上传图片到小红书创作平台
"""

import os
import sys
import shutil
import argparse
from pathlib import Path

def setup_upload_directory(upload_dir="/tmp/openclaw/uploads"):
    """
    设置上传目录
    """
    try:
        # 创建上传目录
        os.makedirs(upload_dir, exist_ok=True)
        print(f"📁 上传目录已创建: {upload_dir}")
        
        # 清理旧文件
        for file in os.listdir(upload_dir):
            file_path = os.path.join(upload_dir, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"⚠️  清理文件失败 {file_path}: {e}")
        
        return upload_dir
    except Exception as e:
        print(f"❌ 设置上传目录失败: {e}")
        return None

def copy_images_to_upload(images, upload_dir):
    """
    复制图片到上传目录
    """
    uploaded_files = []
    
    for img_path in images:
        try:
            # 检查文件是否存在
            if not os.path.exists(img_path):
                print(f"❌ 文件不存在: {img_path}")
                continue
            
            # 检查文件格式
            if not img_path.lower().endswith(('.jpg', '.jpeg', '.png')):
                print(f"⚠️  不支持的文件格式: {img_path}")
                continue
            
            # 复制文件
            filename = os.path.basename(img_path)
            dest_path = os.path.join(upload_dir, filename)
            shutil.copy2(img_path, dest_path)
            
            # 检查文件大小
            file_size = os.path.getsize(dest_path) / (1024 * 1024)  # MB
            if file_size > 32:
                print(f"⚠️  文件过大 ({file_size:.1f}MB > 32MB): {filename}")
                os.unlink(dest_path)
                continue
            
            uploaded_files.append(dest_path)
            print(f"✅ 已复制: {filename} ({file_size:.1f}MB)")
            
        except Exception as e:
            print(f"❌ 复制文件失败 {img_path}: {e}")
    
    return uploaded_files

def prepare_images_for_upload(images_dir=None, image_files=None):
    """
    准备图片用于上传
    """
    upload_dir = setup_upload_directory()
    if not upload_dir:
        return None
    
    images_to_upload = []
    
    # 处理目录
    if images_dir and os.path.isdir(images_dir):
        print(f"📂 扫描目录: {images_dir}")
        for file in sorted(os.listdir(images_dir)):
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                img_path = os.path.join(images_dir, file)
                images_to_upload.append(img_path)
    
    # 处理文件列表
    if image_files:
        images_to_upload.extend(image_files)
    
    if not images_to_upload:
        print("❌ 未找到可上传的图片")
        return None
    
    # 检查图片数量
    if len(images_to_upload) > 18:
        print(f"⚠️  图片数量过多 ({len(images_to_upload)} > 18)，将使用前18张")
        images_to_upload = images_to_upload[:18]
    
    print(f"📊 准备上传 {len(images_to_upload)} 张图片")
    
    # 复制到上传目录
    uploaded_files = copy_images_to_upload(images_to_upload, upload_dir)
    
    if not uploaded_files:
        print("❌ 没有图片成功复制到上传目录")
        return None
    
    print(f"🎉 准备完成！{len(uploaded_files)} 张图片已就绪")
    return uploaded_files

def get_upload_command(uploaded_files):
    """
    生成上传命令
    """
    if not uploaded_files:
        return None
    
    # 构建browser upload命令
    paths_json = "[" + ", ".join([f'"{path}"' for path in uploaded_files]) + "]"
    
    command = f"""
# 使用OpenClaw browser工具上传图片
browser upload \\
  --profile openclaw \\
  --targetId "YOUR_TARGET_ID" \\
  --paths {paths_json}
"""
    
    return command

def main():
    parser = argparse.ArgumentParser(description="小红书图片上传准备脚本")
    parser.add_argument("--images-dir", help="图片目录路径")
    parser.add_argument("--images", nargs="+", help="图片文件列表")
    parser.add_argument("--upload-dir", default="/tmp/openclaw/uploads", 
                       help="上传目录路径（默认: /tmp/openclaw/uploads）")
    
    args = parser.parse_args()
    
    if not args.images_dir and not args.images:
        print("❌ 请指定图片目录或图片文件")
        parser.print_help()
        return 1
    
    print("🚀 小红书图片上传准备工具")
    print("=" * 50)
    
    # 准备图片
    uploaded_files = prepare_images_for_upload(
        images_dir=args.images_dir,
        image_files=args.images
    )
    
    if not uploaded_files:
        return 1
    
    print("\n" + "=" * 50)
    print("📋 上传准备完成")
    print("=" * 50)
    
    # 显示上传文件信息
    print("\n📁 上传目录内容:")
    for file in sorted(uploaded_files):
        filename = os.path.basename(file)
        size = os.path.getsize(file) / 1024  # KB
        print(f"  - {filename} ({size:.1f}KB)")
    
    # 生成上传命令
    upload_cmd = get_upload_command(uploaded_files)
    if upload_cmd:
        print("\n📝 上传命令:")
        print(upload_cmd)
    
    print("\n✅ 准备完成！现在可以使用 browser upload 工具上传图片了。")
    return 0

if __name__ == "__main__":
    sys.exit(main())
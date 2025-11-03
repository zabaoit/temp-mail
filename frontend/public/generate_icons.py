#!/usr/bin/env python3
"""
Script để tạo favicon và logo icons từ SVG
Yêu cầu: pip install cairosvg pillow
"""

import os
import sys

try:
    import cairosvg
    from PIL import Image
    import io
except ImportError:
    print("❌ Thiếu thư viện cần thiết!")
    print("\n📦 Đang cài đặt cairosvg và pillow...")
    os.system(f"{sys.executable} -m pip install cairosvg pillow")
    print("\n✅ Đã cài đặt xong! Vui lòng chạy lại script này.")
    sys.exit(0)

def svg_to_png(svg_path, png_path, size):
    """Convert SVG to PNG with specified size"""
    try:
        cairosvg.svg2png(
            url=svg_path,
            write_to=png_path,
            output_width=size,
            output_height=size
        )
        print(f"✅ Đã tạo: {png_path} ({size}x{size})")
        return True
    except Exception as e:
        print(f"❌ Lỗi tạo {png_path}: {e}")
        return False

def create_favicon_ico(png_paths, ico_path):
    """Create multi-size ICO file from PNG files"""
    try:
        images = []
        for png_path in png_paths:
            if os.path.exists(png_path):
                img = Image.open(png_path)
                images.append(img)
        
        if images:
            images[0].save(
                ico_path,
                format='ICO',
                sizes=[(16, 16), (32, 32), (48, 48), (64, 64)],
                append_images=images[1:] if len(images) > 1 else []
            )
            print(f"✅ Đã tạo: {ico_path}")
            return True
    except Exception as e:
        print(f"❌ Lỗi tạo favicon.ico: {e}")
        return False

def main():
    # Paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    svg_file = os.path.join(script_dir, "mail-icon.svg")
    
    if not os.path.exists(svg_file):
        print(f"❌ Không tìm thấy file SVG: {svg_file}")
        return
    
    print("🎨 Đang tạo favicon và logo icons...")
    print("=" * 50)
    
    # Create different sizes
    temp_pngs = []
    
    # Create 192x192 for mobile
    png_192 = os.path.join(script_dir, "logo192.png")
    if svg_to_png(svg_file, png_192, 192):
        temp_pngs.append(png_192)
    
    # Create 512x512 for high-res
    png_512 = os.path.join(script_dir, "logo512.png")
    if svg_to_png(svg_file, png_512, 512):
        temp_pngs.append(png_512)
    
    # Create 64x64 for favicon
    png_64 = os.path.join(script_dir, "temp_64.png")
    if svg_to_png(svg_file, png_64, 64):
        # Create favicon.ico from 64x64 PNG
        favicon_path = os.path.join(script_dir, "favicon.ico")
        create_favicon_ico([png_64], favicon_path)
        
        # Clean up temp file
        if os.path.exists(png_64):
            os.remove(png_64)
    
    print("=" * 50)
    print("✅ Hoàn thành!")
    print(f"\n📁 Các file đã tạo trong thư mục: {script_dir}")
    print("   - favicon.ico (16x16, 32x32, 48x48, 64x64)")
    print("   - logo192.png (192x192)")
    print("   - logo512.png (512x512)")

if __name__ == "__main__":
    main()

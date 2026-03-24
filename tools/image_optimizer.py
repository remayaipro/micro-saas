#!/usr/bin/env python3
"""Image Optimizer - CLI Tool for compress/resize images"""

import argparse
import os
import sys
from PIL import Image

def optimize_image(input_path, output_path=None, quality=85, max_width=None, max_height=None):
    """Optimize image: compress and/or resize"""
    
    if not os.path.exists(input_path):
        print(f"Error: File not found: {input_path}")
        return 1
    
    # Default output path
    if not output_path:
        name, ext = os.path.splitext(input_path)
        output_path = f"{name}_optimized{ext}"
    
    try:
        with Image.open(input_path) as img:
            # Handle RGBA to RGB conversion for JPEG
            if img.mode in ('RGBA', 'LA') and output_path.lower().endswith(('.jpg', '.jpeg')):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            
            # Resize if dimensions specified
            if max_width or max_height:
                width, height = img.size
                new_width = width
                new_height = height
                
                if max_width and width > max_width:
                    ratio = max_width / width
                    new_width = max_width
                    new_height = int(height * ratio)
                
                if max_height and new_height > max_height:
                    ratio = max_height / new_height
                    new_height = max_height
                    new_width = int(new_width * ratio)
                
                if new_width != width or new_height != height:
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    print(f"Resized: {width}x{height} -> {new_width}x{new_height}")
            
            # Save with compression
            save_kwargs = {'quality': quality, 'optimize': True}
            
            if output_path.lower().endswith('.png'):
                # PNG compression
                img.save(output_path, 'PNG', **save_kwargs)
            else:
                img.save(output_path, 'JPEG', **save_kwargs)
            
            original_size = os.path.getsize(input_path)
            optimized_size = os.path.getsize(output_path)
            savings = ((original_size - optimized_size) / original_size) * 100
            
            print(f"Optimized: {input_path} -> {output_path}")
            print(f"Original: {original_size:,} bytes")
            print(f"Optimized: {optimized_size:,} bytes")
            print(f"Savings: {savings:.1f}%")
            
            return 0
            
    except Exception as e:
        print(f"Error: {e}")
        return 1

def main():
    parser = argparse.ArgumentParser(description='Image Optimizer - Compress/Resize Images')
    parser.add_argument('input', help='Input image file')
    parser.add_argument('-o', '--output', help='Output file (default: input_optimized.ext)')
    parser.add_argument('-q', '--quality', type=int, default=85, help='JPEG quality 1-100 (default: 85)')
    parser.add_argument('-w', '--max-width', type=int, help='Max width in pixels')
    parser.add_argument('-H', '--max-height', type=int, help='Max height in pixels')
    
    args = parser.parse_args()
    
    return optimize_image(
        args.input,
        args.output,
        args.quality,
        args.max_width,
        args.max_height
    )

if __name__ == '__main__':
    exit(main())
"""
Ozon商品截图换背景：
1. 用 rembg 去除原背景
2. 在新背景上合成（纯色渐变背景）
"""

from rembg import remove, new_session
from PIL import Image, ImageFilter
import os

INPUT = r"C:\Users\ASDCF\.qclaw\media\inbound\paste_1781776604120_fpe9yv__orig_ScreenShot_2026-06-18_175556_474.png"
OUTPUT = r"C:\Users\ASDCF\.qclaw\workspace\ozon_product_new_bg.png"

# 读取原图
img = Image.open(INPUT).convert("RGBA")
print(f"Original size: {img.size}, mode: {img.mode}")

# 用 u2net 模型去除背景
session = new_session("u2net")
out = remove(img, session=session, alpha_matting=True,
             alpha_matting_foreground_threshold=240,
             alpha_matting_background_threshold=10,
             alpha_matting_erode_structure_size=1)

print(f"After remove - size: {out.size}, mode: {out.mode}")

# 创建渐变背景 (从上到下: 浅灰蓝 -> 白)
w, h = out.size
bg = Image.new("RGBA", (w, h), (255, 255, 255, 255))

# 绘制一个柔和的渐变背景
for y in range(h):
    ratio = y / h
    r = int(240 - 40 * ratio)
    g = int(245 - 25 * ratio)
    b = int(255 - 30 * ratio)
    for x in range(w):
        bg.putpixel((x, y), (r, g, b, 255))

# 合成：前景放在背景上
composite = Image.alpha_composite(bg, out)

# 转为 RGB 保存
result = composite.convert("RGB")
result.save(OUTPUT, quality=95)
print(f"Saved to: {OUTPUT}")
print("Done!")

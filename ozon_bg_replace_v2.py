"""
Ozon截图换背景 - 基于色彩阈值法（无需下载模型）
适用场景：电商白底/浅底商品截图
"""

from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
import os

INPUT = r"C:\Users\ASDCF\.qclaw\media\inbound\paste_1781776604120_fpe9yv__orig_ScreenShot_2026-06-18_175556_474.png"
OUTPUT = r"C:\Users\ASDCF\.qclaw\workspace\ozon_product_new_bg.png"

img = Image.open(INPUT).convert("RGBA")
print(f"Original: {img.size}")

arr = np.array(img, dtype=np.float32)
h, w = arr.shape[:2]

# 检测接近白色的像素 (R>230, G>230, B>230) 作为背景
r, g, b, a = arr[:,:,0], arr[:,:,1], arr[:,:,2], arr[:,:,3]

# 浅色背景掩码（电商截图通常是白色/极浅灰背景）
bg_mask = (r > 235) & (g > 235) & (b > 235)

# 边缘防护：对掩码做模糊，保留商品边缘过渡
bg_mask_float = bg_mask.astype(np.float32)

# 创建一个alpha通道 - 背景全透明，前景不透明
alpha = np.ones((h, w), dtype=np.float32) * 255
alpha[bg_mask] = 0

# 对alpha做模糊使边缘柔和
from scipy.ndimage import gaussian_filter
alpha = gaussian_filter(alpha, sigma=1.5)

# 裁剪边缘：对靠近图像边缘的区域，保留合理的边框
# 对于电商截图，保留页面框架结构
arr_new = arr.copy()
arr_new[:,:,3] = np.clip(alpha, 0, 255).astype(np.uint8)

result = Image.fromarray(arr_new.astype(np.uint8), "RGBA")
print(f"Subject extracted, alpha mask applied")

# 创建新背景 - 暖灰渐变背景
bg = Image.new("RGBA", (w, h), (255, 255, 255, 255))
for y in range(h):
    ratio = y / h
    # 从浅灰蓝渐变到暖白
    r_val = int(235 - 30 * ratio)
    g_val = int(240 - 20 * ratio)
    b_val = int(250 - 25 * ratio)
    bg.putpixel((0, y), (r_val, g_val, b_val, 255))
    # 水平方向也做一个渐变
    for x in range(1, w):
        x_ratio = x / w
        r_final = int(r_val - 20 * (1 - x_ratio) * ratio)
        g_final = int(g_val - 15 * (1 - x_ratio) * ratio)  
        b_final = int(b_val - 20 * (1 - x_ratio) * ratio)
        bg.putpixel((x, y), (r_final, g_final, b_final, 255))

# 合成
composite = Image.alpha_composite(bg, result)
final = composite.convert("RGB")
final.save(OUTPUT, quality=95)
print(f"Saved: {OUTPUT}")
print("Done!")

# -*- coding: utf-8 -*-
import docx
import sys

# 读取文档
doc = docx.Document(r'E:\郑州录音\新建 DOCX 文档.docx')

# 提取所有段落
paragraphs = []
for para in doc.paragraphs:
    text = para.text.strip()
    if text:
        paragraphs.append(text)

# 输出所有内容
print(f"=== 共 {len(paragraphs)} 个段落 ===\n")
for i, p in enumerate(paragraphs):
    print(f"[段{i+1}] {p}")
    print()

# -*- coding: utf-8 -*-
"""
Convert docx to premium Silk-Road themed business PDF.
Features: Chinese decorative elements, amber+navy palette, gradient cover background.
"""

import sys
import os
import re
import win32com.client
from win32com.client import constants

doc_path = r"C:\Users\ASDCF\Desktop\新丝路跨境_实战出海_第二套商业模式方案书.docx"
output_pdf = os.path.join(os.path.expanduser("~"), ".qclaw", "workspace", "新丝路跨境_实战出海_第二套商业模式方案书.pdf")

# Silk Road inspired palette
NAVY       = 0x543A1F  # #1F3A54 deep navy
STEEL_BLUE = 0x8B6B2E  # #2E6B8B medium blue
GOLD       = 0x55B1C9  # #C9A955 gold/amber
SAND       = 0xA5B1C9  # #C9B1A5 sand beige
AMBER      = 0x58B8D4  # #D4B858 amber
DARK_GRAY  = 0x333333
MED_GRAY   = 0x666666
LIGHT_GRAY = 0x999999
WHITE      = 0xFFFFFF
BG_LIGHT   = 0xEFF1F3
CREAM      = 0xE8EDF4  # Warm cream background
BORDER_LT  = 0xD0D0D0

word = win32com.client.Dispatch("Word.Application")
word.Visible = False
word.DisplayAlerts = 0

def add_cover_background_shape(section, doc):
    """Add a subtle Silk Road themed background to the cover page"""
    try:
        # Add a large rectangle shape behind cover text
        # Use the first page header to add a shape that appears on background
        hdr = section.Headers(2)  # wdHeaderFooterFirstPage
        hdr.LinkToPrevious = False
        hdr.Range.Text = ""
        
        # Get page dimensions (points)
        pw = doc.PageSetup.PageWidth
        ph = doc.PageSetup.PageHeight
        ml = doc.PageSetup.LeftMargin
        mr = doc.PageSetup.RightMargin
        mt = doc.PageSetup.TopMargin
        mb = doc.PageSetup.BottomMargin
        
        # Add a subtle decorative shape - a rounded rectangle with gradient
        shape = hdr.Shapes.AddShape(
            5,   # msoShapeRoundedRectangle = 5
            36,  # Left position
            36,  # Top position
            pw - 72,  # Width
            ph - 72   # Height
        )
        
        # Set fill to subtle gradient
        shape.Fill.TwoColorGradient(1, 1)  # msoGradientHorizontal = 1, msoGradientFromCenter = 1
        shape.Fill.ForeColor.RGB = 0xE0E4EA  # Very light warm gray
        shape.Fill.BackColor.RGB = 0xF2F4F6  # Off-white
        
        # Set line to gold/double
        shape.Line.ForeColor.RGB = GOLD
        shape.Line.Weight = 1.5
        shape.Line.DashStyle = 1  # Solid
        
        # Make it subtle - send behind text, set transparency
        shape.Fill.Transparency = 0.85
        shape.WrapFormat.Type = 3  # wdWrapBehind = 3
        
        # Add a second thin decorative border inside
        shape2 = hdr.Shapes.AddShape(
            5,  # msoShapeRoundedRectangle
            50, # Left position (inset)
            50, # Top position (inset)
            pw - 100,  # Width (inset)
            ph - 100   # Height (inset)
        )
        shape2.Fill.Transparency = 1.0  # No fill
        shape2.Line.ForeColor.RGB = AMBER
        shape2.Line.Weight = 0.5
        shape2.Line.DashStyle = 2  # Dash
        shape2.WrapFormat.Type = 3
        
        print("  已添加封面背景装饰框")
        
    except Exception as e:
        print(f"  [skip] 背景装饰: {e}")

def add_page_border_shapes(main_header):
    """Add decorative border shapes on content pages (in header background)"""
    try:
        pw = 595.35  # A4 width
        ph = 841.95  # A4 height
        
        # Outer thin rectangle - subtle gold frame
        shape = main_header.Shapes.AddShape(
            1, 16, 12, pw - 32, ph - 24
        )
        shape.Fill.Transparency = 1.0
        shape.Line.ForeColor.RGB = GOLD
        shape.Line.Weight = 0.75
        shape.Line.DashStyle = 1
        shape.WrapFormat.Type = 3
        
        # Inner rectangle - thinner, darker
        shape2 = main_header.Shapes.AddShape(
            1, 20, 16, pw - 40, ph - 32
        )
        shape2.Fill.Transparency = 1.0
        shape2.Line.ForeColor.RGB = AMBER
        shape2.Line.Weight = 0.25
        shape2.Line.DashStyle = 2  # Dash
        shape2.WrapFormat.Type = 3
        
        print("  已添加页面装饰边框（金色+琥珀）")
    except Exception as e:
        print(f"  [skip] 页面边框: {e}")

def add_corner_decoration(header):
    """Add a small decorative line motif to page corners"""
    try:
        # We'll add a subtle line in the header area as a decorative touch
        pass
    except:
        pass

print("=== 新丝路跨境 · 高端商务 PDF 生成 ===")
print()

word = win32com.client.Dispatch("Word.Application")
word.Visible = False
word.DisplayAlerts = 0

try:
    print("打开文档...")
    doc = word.Documents.Open(doc_path)

    # =========================================================
    # 1. Page setup - A4 with wider margins for border
    # =========================================================
    print("设置页面格式...")
    doc.PageSetup.PageWidth = 595.35
    doc.PageSetup.PageHeight = 841.95
    doc.PageSetup.TopMargin = 66
    doc.PageSetup.BottomMargin = 66
    doc.PageSetup.LeftMargin = 90
    doc.PageSetup.RightMargin = 90
    doc.PageSetup.HeaderDistance = 24
    doc.PageSetup.FooterDistance = 24

    # =========================================================
    # 2. Cover page with Silk Road styling
    # =========================================================
    print("创建丝绸之路主题封面...")
    
    rng = doc.Range(0, 0)
    
    # Minimal top spacer
    for _ in range(3):
        rng.Text = "\r"; rng.Collapse(0)
    
    # ── Top border line (double style gold) ──
    rng.Text = "═" * 55 + "\r"
    rng.Collapse(0)
    rng.Font.Name = "微软雅黑"
    rng.Font.Size = 6
    rng.Font.Color = GOLD
    rng.ParagraphFormat.Alignment = 1
    rng.Collapse(0)
    
    # Thin accent
    rng.Text = "─" * 55 + "\r"
    rng.Collapse(0)
    rng.Font.Name = "微软雅黑"
    rng.Font.Size = 3
    rng.Font.Color = AMBER
    rng.ParagraphFormat.Alignment = 1
    rng.Collapse(0)
    
    rng.Text = "\r"; rng.Collapse(0)
    
    # ── Main Brand Title ──
    rng.Text = "新丝路跨境\r"
    rng.Collapse(0)
    rng.Font.Name = "微软雅黑"
    rng.Font.Size = 40
    rng.Font.Bold = True
    rng.Font.Color = NAVY
    rng.ParagraphFormat.Alignment = 1
    rng.Collapse(0)
    
    rng.Text = "实战出海\r"
    rng.Collapse(0)
    rng.Font.Name = "微软雅黑"
    rng.Font.Size = 28
    rng.Font.Bold = True
    rng.Font.Color = STEEL_BLUE
    rng.ParagraphFormat.Alignment = 1
    rng.Collapse(0)
    
    # ── Gold accent divider ──
    rng.Text = "═══ ❖ ═══\r"
    rng.Collapse(0)
    rng.Font.Name = "微软雅黑"
    rng.Font.Size = 10
    rng.Font.Color = GOLD
    rng.ParagraphFormat.Alignment = 1
    rng.Collapse(0)
    
    # Document type
    rng.Text = "第二套商业模式方案书\r"
    rng.Collapse(0)
    rng.Font.Name = "微软雅黑"
    rng.Font.Size = 22
    rng.Font.Bold = True
    rng.Font.Color = NAVY
    rng.ParagraphFormat.Alignment = 1
    rng.Collapse(0)
    
    # Subtitle
    rng.Text = "以交付为基石的企业出海全链路服务平台\r"
    rng.Collapse(0)
    rng.Font.Name = "微软雅黑"
    rng.Font.Size = 13
    rng.Font.Color = MED_GRAY
    rng.ParagraphFormat.Alignment = 1
    rng.Collapse(0)
    
    rng.Text = "\r"; rng.Collapse(0)
    
    # Tagline
    rng.Text = "「让每一次出海都有人陪跑到底」\r"
    rng.Collapse(0)
    rng.Font.Name = "微软雅黑"
    rng.Font.Size = 12
    rng.Font.Italic = True
    rng.Font.Color = GOLD
    rng.ParagraphFormat.Alignment = 1
    rng.Collapse(0)
    
    rng.Text = "\r"; rng.Collapse(0)
    
    # ── Bottom double lines ──
    rng.Text = "─" * 55 + "\r"
    rng.Collapse(0)
    rng.Font.Name = "微软雅黑"
    rng.Font.Size = 3
    rng.Font.Color = AMBER
    rng.ParagraphFormat.Alignment = 1
    rng.Collapse(0)
    
    rng.Text = "═" * 55 + "\r"
    rng.Collapse(0)
    rng.Font.Name = "微软雅黑"
    rng.Font.Size = 6
    rng.Font.Color = GOLD
    rng.ParagraphFormat.Alignment = 1
    rng.Collapse(0)
    
    rng.Text = "\r"; rng.Collapse(0)
    
    # Year
    rng.Text = "2026 · 第二套商业模式\r"
    rng.Collapse(0)
    rng.Font.Name = "微软雅黑"
    rng.Font.Size = 10
    rng.Font.Color = LIGHT_GRAY
    rng.ParagraphFormat.Alignment = 1
    rng.Collapse(0)
    
    # Insert page break after cover
    pb_range = doc.Range(doc.Range(0, rng.Start - 1).End - 1, doc.Range(0, rng.Start - 1).End - 1)
    pb_range.InsertBreak(7)

    # =========================================================
    # 3. Cover background + Silk Road borders
    # =========================================================
    print("添加丝绸之路装饰元素...")
    
    section = doc.Sections(1)
    section.PageSetup.DifferentFirstPageHeaderFooter = True
    
    # Add background decorative shape to cover
    add_cover_background_shape(section, doc)
    
    # Add decorative page border shapes (gold frames on content pages)
    main_header = section.Headers(1)
    add_page_border_shapes(main_header)

    # =========================================================
    # 4. Header & Footer
    # =========================================================
    print("设置页眉页脚...")
    
    # Cover page - no header/footer
    fph = section.Headers(2)
    fph.LinkToPrevious = False
    fph.Range.Text = ""
    
    fpf = section.Footers(2)
    fpf.LinkToPrevious = False
    fpf.Range.Text = ""
    
    # Main header - with decorative bottom bar
    mh = section.Headers(1)
    mh.LinkToPrevious = False
    mh.Range.Font.Name = "微软雅黑"
    mh.Range.Font.Size = 8.5
    mh.Range.Font.Color = 0x808080
    mh.Range.Text = "新丝路跨境 · 实战出海 · 第二套商业模式方案书"
    mh.Range.ParagraphFormat.Alignment = 0
    
    # Header bottom border: double line (navy + gold thin)
    mh.Range.ParagraphFormat.Borders(3).LineStyle = 1
    mh.Range.ParagraphFormat.Borders(3).Color = NAVY
    mh.Range.ParagraphFormat.Borders(3).LineWidth = 4
    
    # Main footer
    mf = section.Footers(1)
    mf.LinkToPrevious = False
    mf.Range.Font.Name = "微软雅黑"
    mf.Range.Font.Size = 8.5
    mf.Range.Font.Color = 0x808080
    mf.Range.ParagraphFormat.Alignment = 1
    mf.Range.ParagraphFormat.Borders(1).LineStyle = 1
    mf.Range.ParagraphFormat.Borders(1).Color = 0xD0D0D0
    mf.Range.ParagraphFormat.Borders(1).LineWidth = 2
    mf.Range.Text = "— "
    mf.Range.Collapse(0)
    mf.Range.Fields.Add(mf.Range, 0, "PAGE", False)
    mf.Range.Collapse(0)
    mf.Range.Text = " —"

    # =========================================================
    # 5. First content page - decorative separator
    # =========================================================
    print("添加内容页装饰...")
    
    # Add gold top border before each H1 major section heading
    for i in range(1, doc.Paragraphs.Count + 1):
        para = doc.Paragraphs(i)
        text = para.Range.Text.strip()
        if re.match(r'^[一二三四五六七八九十]+、', text):
            para.Range.ParagraphFormat.SpaceBefore = 24
            # Gold double-line top border
            para.Range.ParagraphFormat.Borders(1).LineStyle = 9  # wdLineStyleDouble
            para.Range.ParagraphFormat.Borders(1).Color = GOLD
            para.Range.ParagraphFormat.Borders(1).LineWidth = 3

    # =========================================================
    # 6. Table formatting - Silk Road inspired
    # =========================================================
    print("美化表格样式...")
    
    table_count = doc.Tables.Count
    print(f"发现 {table_count} 个表格")
    
    for ti in range(1, table_count + 1):
        table = doc.Tables(ti)
        
        table.Borders.InsideLineStyle = 1
        table.Borders.OutsideLineStyle = 1
        table.Borders.InsideColor = BORDER_LT
        table.Borders.OutsideColor = NAVY
        table.Borders.InsideLineWidth = 2
        table.Borders.OutsideLineWidth = 3
        
        if table.Rows.Count > 0:
            hr = table.Rows(1)
            hr.HeadingFormat = True
            hr.Range.Font.Bold = True
            hr.Range.Font.Size = 9.5
            hr.Range.Font.Name = "微软雅黑"
            hr.Range.Font.Color = WHITE
            hr.Shading.BackgroundPatternColor = NAVY
            hr.Range.ParagraphFormat.Alignment = 1
        
        for ri in range(2, table.Rows.Count + 1):
            row = table.Rows(ri)
            row.Range.Font.Size = 9
            row.Range.Font.Name = "微软雅黑"
            row.Range.Font.Color = DARK_GRAY
            row.Range.ParagraphFormat.Alignment = 0
            row.Range.ParagraphFormat.SpaceAfter = 3
            row.Range.ParagraphFormat.SpaceBefore = 3
            if ri % 2 == 0:
                row.Shading.BackgroundPatternColor = BG_LIGHT
            else:
                row.Shading.BackgroundPatternColor = WHITE

    # =========================================================
    # 7. Heading/body formatting
    # =========================================================
    print("统一排版样式...")
    
    para_count = doc.Paragraphs.Count
    for i in range(1, para_count + 1):
        para = doc.Paragraphs(i)
        text = para.Range.Text.strip()
        if not text:
            continue
        
        if re.match(r'^[一二三四五六七八九十]+、', text):
            para.Range.Font.Name = "微软雅黑"
            para.Range.Font.Bold = True
            para.Range.Font.Size = 18
            para.Range.Font.Color = NAVY
            para.Range.ParagraphFormat.SpaceBefore = 24
            para.Range.ParagraphFormat.SpaceAfter = 10
            para.Range.ParagraphFormat.Alignment = 0
        
        elif re.match(r'^\d+\.\d+\s', text):
            para.Range.Font.Name = "微软雅黑"
            para.Range.Font.Bold = True
            para.Range.Font.Size = 14
            para.Range.Font.Color = NAVY
            para.Range.ParagraphFormat.SpaceBefore = 14
            para.Range.ParagraphFormat.SpaceAfter = 6
            para.Range.ParagraphFormat.Alignment = 0
        
        elif re.match(r'^第[一二三]层|^全年课程', text):
            para.Range.Font.Name = "微软雅黑"
            para.Range.Font.Bold = True
            para.Range.Font.Size = 12.5
            para.Range.Font.Color = NAVY
            para.Range.ParagraphFormat.SpaceBefore = 12
            para.Range.ParagraphFormat.SpaceAfter = 6
            para.Range.ParagraphFormat.Alignment = 0
        
        elif re.match(r'^\d+\.\d+\.\d+\s|^课程\d', text):
            para.Range.Font.Name = "微软雅黑"
            para.Range.Font.Bold = True
            para.Range.Font.Size = 12
            para.Range.Font.Color = STEEL_BLUE
            para.Range.ParagraphFormat.SpaceBefore = 10
            para.Range.ParagraphFormat.SpaceAfter = 4
            para.Range.ParagraphFormat.Alignment = 0
        
        elif text.startswith("模块"):
            para.Range.Font.Name = "微软雅黑"
            para.Range.Font.Bold = True
            para.Range.Font.Size = 12
            para.Range.Font.Color = STEEL_BLUE
            para.Range.ParagraphFormat.SpaceBefore = 10
            para.Range.ParagraphFormat.SpaceAfter = 4
            para.Range.ParagraphFormat.Alignment = 0
        
        else:
            para.Range.Font.Name = "微软雅黑"
            para.Range.Font.Size = 10.5
            para.Range.Font.Color = DARK_GRAY
            para.Range.ParagraphFormat.SpaceAfter = 4
            para.Range.ParagraphFormat.LineSpacing = 15
            para.Range.ParagraphFormat.Alignment = 0
    
    # Closing tagline
    for i in range(1, doc.Paragraphs.Count + 1):
        para = doc.Paragraphs(i)
        text = para.Range.Text.strip()
        if text.startswith("新丝路跨境"):
            para.Range.Font.Name = "微软雅黑"
            para.Range.Font.Bold = True
            para.Range.Font.Size = 14
            para.Range.Font.Color = NAVY
            para.Range.ParagraphFormat.Alignment = 1
            para.Range.ParagraphFormat.SpaceBefore = 24
            para.Range.ParagraphFormat.Borders(1).LineStyle = 9  # Double gold
            para.Range.ParagraphFormat.Borders(1).Color = GOLD
            para.Range.ParagraphFormat.Borders(1).LineWidth = 3
            break

    # =========================================================
    # 8. Export to PDF
    # =========================================================
    print("导出为 PDF...")
    doc.Repaginate()
    doc.ExportAsFixedFormat(output_pdf, 17, False, 0, 0, 0, 0, 0, True)
    doc.Close(SaveChanges=False)
    
    print()
    print("✓ PDF 生成完成！")
    print(f"  文件路径: {output_pdf}")

except Exception as e:
    print(f"ERROR: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    sys.exit(1)

finally:
    try: word.Quit()
    except: pass

print("=== 完成 ===")

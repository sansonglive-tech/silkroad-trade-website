#Requires -Version 5.1
$ErrorActionPreference = "Stop"

$docPath = "C:\Users\ASDCF\Desktop\新丝路跨境_实战出海_第二套商业模式方案书.docx"
$outputDir = "C:\Users\ASDCF\.qclaw\workspace"
$outputPdf = Join-Path $outputDir "新丝路跨境_实战出海_第二套商业模式方案书.pdf"

Write-Host "=== 启动 Word COM 自动化 ===" -ForegroundColor Cyan

try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0  # wdAlertsNone

    Write-Host "打开文档..." -ForegroundColor Cyan
    $doc = $word.Documents.Open($docPath)

    # =========================================================
    # 1. 页面设置 - A4
    # =========================================================
    Write-Host "设置页面格式..." -ForegroundColor Cyan
    $doc.PageSetup.PageWidth = 595.35   # A4 width in points
    $doc.PageSetup.PageHeight = 841.95  # A4 height in points
    $doc.PageSetup.TopMargin = 72
    $doc.PageSetup.BottomMargin = 72
    $doc.PageSetup.LeftMargin = 90
    $doc.PageSetup.RightMargin = 90
    $doc.PageSetup.HeaderDistance = 28
    $doc.PageSetup.FooterDistance = 28

    # =========================================================
    # 2. 创建专业封面页（作为新节插入到文档开头）
    # =========================================================
    Write-Host "创建高端封面页..." -ForegroundColor Cyan
    
    # Insert a section break at the beginning
    $range = $doc.Range(0, 0)
    $range.InsertBreak(8)  # wdSectionBreakNextPage = 8
    
    # Now the first section is the cover page
    $coverSection = $doc.Sections.Item(1)
    
    # Cover page settings - no header/footer for cover
    $coverSection.Headers.Item(1).LinkToPrevious = $false
    $coverSection.Footers.Item(1).LinkToPrevious = $false
    
    # Suppress header/footer on cover page
    $coverPageSetup = $coverSection.PageSetup
    $coverPageSetup.DifferentFirstPageHeaderFooter = 0
    
    # Get the first page (cover) range
    $coverRange = $doc.Range(0, 0)
    $coverRange.Expand(4)  # wdParagraph
    $coverRange.Collapse(0)  # wdCollapseEnd
    
    # Clear existing empty paragraph
    $coverRange.Text = ""
    
    # Build cover page content
    # Top spacer
    for ($s = 0; $s -lt 6; $s++) {
        $coverRange.Text = "`r"
        $coverRange.Collapse(0)
    }
    
    # ------- Main Title -------
    $coverRange.Text = "新丝路跨境" + "`r"
    $coverRange.Collapse(0)
    $coverRange.Font.Name = "微软雅黑"
    $coverRange.Font.Size = 36
    $coverRange.Font.Bold = 1
    $coverRange.Font.Color = [int]2059065  # Deep navy #1F4E79
    $coverRange.ParagraphFormat.Alignment = 1  # Center
    
    # Subtitle
    $coverRange.Text = "实战出海" + "`r"
    $coverRange.Collapse(0)
    $coverRange.Font.Name = "微软雅黑"
    $coverRange.Font.Size = 28
    $coverRange.Font.Color = [int]3051108  # #2E75B6
    $coverRange.ParagraphFormat.Alignment = 1
    
    # Decorative line
    $coverRange.Text = "━━━━━━━━━━━━━━━━━━━━" + "`r"
    $coverRange.Collapse(0)
    $coverRange.Font.Size = 14
    $coverRange.Font.Color = [int]12632256  # Gray
    $coverRange.ParagraphFormat.Alignment = 1
    
    # Document type
    $coverRange.Text = "商业模式方案书" + "`r"
    $coverRange.Collapse(0)
    $coverRange.Font.Name = "微软雅黑"
    $coverRange.Font.Size = 20
    $coverRange.Font.Bold = 1
    $coverRange.Font.Color = [int]2059065  # #1F4E79
    $coverRange.ParagraphFormat.Alignment = 1
    
    # Subtitle line 2
    $coverRange.Text = "以交付为基石的企业出海全链路服务平台" + "`r"
    $coverRange.Collapse(0)
    $coverRange.Font.Name = "微软雅黑"
    $coverRange.Font.Size = 14
    $coverRange.Font.Color = [int]6710886  # Dark gray #666666
    $coverRange.ParagraphFormat.Alignment = 1
    
    # Spacer
    $coverRange.Text = "`r"
    $coverRange.Collapse(0)
    $coverRange.Text = "`r"
    $coverRange.Collapse(0)
    
    # Tagline
    $coverRange.Text = "—— 让每一次出海都有人陪跑到底 ——" + "`r"
    $coverRange.Collapse(0)
    $coverRange.Font.Name = "微软雅黑"
    $coverRange.Font.Size = 12
    $coverRange.Font.Italic = 1
    $coverRange.Font.Color = [int]10066329  # Medium gray #999999
    $coverRange.ParagraphFormat.Alignment = 1
    
    # Push to bottom
    for ($s = 0; $s -lt 18; $s++) {
        $coverRange.Text = "`r"
        $coverRange.Collapse(0)
    }
    
    # Bottom info line
    $coverRange.Text = "2026 年度 · 第二套商业模式" + "`r"
    $coverRange.Collapse(0)
    $coverRange.Font.Name = "微软雅黑"
    $coverRange.Font.Size = 10
    $coverRange.Font.Color = [int]12632256  # Gray
    $coverRange.ParagraphFormat.Alignment = 1

    # =========================================================
    # 3. 设置主文档节的页眉页脚
    # =========================================================
    Write-Host "设置页眉页脚..." -ForegroundColor Cyan
    
    # The content is now in Section 2
    $mainSection = $doc.Sections.Item(2)
    $mainSection.Headers.Item(1).LinkToPrevious = $false
    $mainSection.Footers.Item(1).LinkToPrevious = $false
    
    # ---- Header ----
    $headerRange = $mainSection.Headers.Item(1).Range
    $headerRange.Text = ""
    $headerRange.Font.Name = "微软雅黑"
    $headerRange.Font.Size = 8.5
    $headerRange.Font.Color = [int]12632256  # Gray
    $headerRange.Font.Italic = 1
    $headerRange.Text = "新丝路跨境 · 实战出海 · 第二套商业模式方案书"
    $headerRange.ParagraphFormat.Alignment = 0  # Left
    
    # Header bottom border (thin line)
    $headerRange.ParagraphFormat.Borders.Item(3).LineStyle = 1  # wdLineStyleSingle = 1
    $headerRange.ParagraphFormat.Borders.Item(3).Color = [int]14211288  # Light gray
    $headerRange.ParagraphFormat.Borders.Item(3).LineWidth = 2  # 0.5pt
    
    # ---- Footer ----
    $footerRange = $mainSection.Footers.Item(1).Range
    $footerRange.Text = ""
    $footerRange.Font.Name = "微软雅黑"
    $footerRange.Font.Size = 8.5
    $footerRange.Font.Color = [int]12632256  # Gray
    
    # Footer top border
    $footerRange.ParagraphFormat.Borders.Item(1).LineStyle = 1  # Top border
    $footerRange.ParagraphFormat.Borders.Item(1).Color = [int]14211288
    $footerRange.ParagraphFormat.Borders.Item(1).LineWidth = 2
    
    # Page number (center)
    $footerRange.ParagraphFormat.Alignment = 1  # Center
    $footerRange.Text = "— "
    $footerRange.Collapse(0)
    $pageField = $footerRange.Fields.Add($footerRange, 0, "PAGE", $false)
    $footerRange.Collapse(0)
    $footerRange.Text = " —"
    
    # Set first page header/footer (for section 2)
    $mainSection.PageSetup.DifferentFirstPageHeaderFooter = 1
    $firstPageHeader = $mainSection.Headers.Item(2)  # wdHeaderFooterFirstPage = 2
    $firstPageHeader.LinkToPrevious = $false
    $firstPageHeader.Range.Text = ""
    $firstPageFooter = $mainSection.Footers.Item(2)
    $firstPageFooter.LinkToPrevious = $false
    $firstPageFooter.Range.Text = ""

    # =========================================================
    # 4. 增强表格样式 - 专业商务表格
    # =========================================================
    Write-Host "美化表格样式..." -ForegroundColor Cyan
    
    # Table colors
    $headerBg = [int]2059065     # #1F4E79 deep navy
    $headerFg = [int]16777215    # White
    $altRowBg = [int]15263976    # #E8EDF2 light blue-gray
    $borderColor = [int]12632256 # Gray
    
    $tableCount = $doc.Tables.Count
    Write-Host "发现 $tableCount 个表格" -ForegroundColor Cyan
    
    for ($ti = 1; $ti -le $tableCount; $ti++) {
        $table = $doc.Tables.Item($ti)
        
        # Apply borders to entire table
        $table.Borders.InsideLineStyle = 1
        $table.Borders.OutsideLineStyle = 1
        $table.Borders.InsideColor = [int]14211288  # Light gray
        $table.Borders.OutsideColor = [int]12632256  # Gray
        $table.Borders.InsideLineWidth = 2  # 0.5pt
        $table.Borders.OutsideLineWidth = 3  # 1pt
        
        # Header row formatting
        $headerRow = $table.Rows.Item(1)
        $headerRow.HeadingFormat = 1
        $headerRow.Range.Font.Bold = 1
        $headerRow.Range.Font.Size = 9.5
        $headerRow.Range.Font.Name = "微软雅黑"
        $headerRow.Range.Font.Color = [int]16777215  # White
        
        # Check if header already has shading
        $headerRow.Shading.BackgroundPatternColor = [int]2059065  # #1F4E79
        
        # Center align header row
        $headerRow.Range.ParagraphFormat.Alignment = 1  # Center
        
        # Data rows
        $rowCount = $table.Rows.Count
        for ($ri = 2; $ri -le $rowCount; $ri++) {
            $row = $table.Rows.Item($ri)
            $row.Range.Font.Size = 9
            $row.Range.Font.Name = "微软雅黑"
            $row.Range.Font.Color = [int]3355443  # #333333 dark gray
            $row.Range.ParagraphFormat.Alignment = 0  # Left
            $row.Range.ParagraphFormat.SpaceAfter = 3
            $row.Range.ParagraphFormat.SpaceBefore = 3
            
            # Alternating row colors
            if ($ri % 2 -eq 0) {
                $row.Shading.BackgroundPatternColor = [int]15987699  # #F4F6F8 very light
            } else {
                $row.Shading.BackgroundPatternColor = [int]16777215  # White
            }
        }
    }

    # =========================================================
    # 5. 强化标题样式一致性
    # =========================================================
    Write-Host "统一标题样式..." -ForegroundColor Cyan
    
    # Process all paragraphs to standardize heading formatting
    $paraCount = $doc.Paragraphs.Count
    for ($i = 1; $i -le $paraCount; $i++) {
        $para = $doc.Paragraphs.Item($i)
        $text = $para.Range.Text.Trim()
        if ([string]::IsNullOrEmpty($text)) { continue }
        
        # Detect and reinforce heading styles
        if ($text -match '^[一二三四五六七八九十]+、') {
            $para.Range.Font.Name = "微软雅黑"
            $para.Range.Font.Bold = 1
            $para.Range.Font.Size = 18
            $para.Range.Font.Color = [int]2059065  # #1F4E79
            $para.Range.ParagraphFormat.SpaceBefore = 18
            $para.Range.ParagraphFormat.SpaceAfter = 10
            $para.Range.ParagraphFormat.Alignment = 0  # Left
        } elseif ($text -match '^\d+\.\d+\s') {
            # Level 2 headings
            $para.Range.Font.Name = "微软雅黑"
            $para.Range.Font.Bold = 1
            $para.Range.Font.Size = 14
            $para.Range.Font.Color = [int]3051108  # #2E75B6
            $para.Range.ParagraphFormat.SpaceBefore = 14
            $para.Range.ParagraphFormat.SpaceAfter = 6
        } elseif ($text -match '^[课程模块]') {
            $para.Range.Font.Name = "微软雅黑"
            $para.Range.Font.Bold = 1
            $para.Range.Font.Size = 12
            $para.Range.Font.Color = [int]2059065  # #1F4E79
            $para.Range.ParagraphFormat.SpaceBefore = 10
            $para.Range.ParagraphFormat.SpaceAfter = 4
        } elseif ($text -match '^\d+\.\d+\.\d+\s') {
            # Level 3 headings
            $para.Range.Font.Name = "微软雅黑"
            $para.Range.Font.Bold = 1
            $para.Range.Font.Size = 12
            $para.Range.Font.Color = [int]3051108  # #2E75B6
            $para.Range.ParagraphFormat.SpaceBefore = 10
            $para.Range.ParagraphFormat.SpaceAfter = 4
        } elseif ($text -match '^第一层|^第二层|^第三层|^全年课') {
            # Section sub-titles (like "第一层：99元门票课")
            $para.Range.Font.Name = "微软雅黑"
            $para.Range.Font.Bold = 1
            $para.Range.Font.Size = 12.5
            $para.Range.Font.Color = [int]2059065  # #1F4E79
            $para.Range.ParagraphFormat.SpaceBefore = 12
            $para.Range.ParagraphFormat.SpaceAfter = 6
        } else {
            # Body text - consistent formatting
            if ($para.Range.Font.Bold -eq -1) {
                # Already bold (key terms), just ensure font
                $para.Range.Font.Name = "微软雅黑"
                $para.Range.Font.Size = 10.5
            } else {
                $para.Range.Font.Name = "微软雅黑"
                $para.Range.Font.Size = 10.5
                $para.Range.Font.Color = [int]3355443  # #333333
            }
            $para.Range.ParagraphFormat.SpaceAfter = 4
            $para.Range.ParagraphFormat.LineSpacing = 15  # 1.15 line spacing
            $para.Range.ParagraphFormat.Alignment = 0  # Left
        }
    }

    # =========================================================
    # 6. 最终段落处理
    # =========================================================
    Write-Host "规范化正文排版..." -ForegroundColor Cyan
    
    # Check for the closing statement
    for ($i = 1; $i -le $doc.Paragraphs.Count; $i++) {
        $para = $doc.Paragraphs.Item($i)
        $text = $para.Range.Text.Trim()
        if ($text -match "^新丝路跨境") {
            $para.Range.Font.Name = "微软雅黑"
            $para.Range.Font.Bold = 1
            $para.Range.Font.Size = 14
            $para.Range.Font.Color = [int]2059065  # #1F4E79
            $para.Range.ParagraphFormat.Alignment = 1  # Center
            $para.Range.ParagraphFormat.SpaceBefore = 20
        }
    }

    # =========================================================
    # 7. 导出为 PDF
    # =========================================================
    Write-Host "导出为 PDF..." -ForegroundColor Cyan
    
    # Clean up empty paragraphs on cover page by adjusting sections
    $doc.Repaginate()
    
    # Set print quality
    $doc.PrintPreview = $false
    
    # Export to PDF
    # wdExportFormatPDF = 17
    # wdExportOptimizeForPrint = 0
    # wdExportRangeAllDocument = 0
    # wdExportDocumentContent = 0
    
    $doc.ExportAsFixedFormat(
        $outputPdf,
        17,           # wdExportFormatPDF
        $false,       # Open after export
        0,            # wdExportOptimizeForPrint
        [ref]0,       # Range (wdExportRangeAllDocument)
        [ref]0,       # Start page
        [ref]0,       # End page
        [ref]0,       # Item (wdExportDocumentContent)
        [ref]$true    # Include doc properties
    )
    
    $doc.Close($false)
    
    Write-Host ""
    Write-Host "✓ PDF 生成完成！" -ForegroundColor Green
    Write-Host "  文件路径: $outputPdf" -ForegroundColor Yellow
    
} catch {
    Write-Host "ERROR: $_" -ForegroundColor Red
    Write-Host $_.ScriptStackTrace -ForegroundColor Red
} finally {
    if ($doc) {
        try { $doc.Close($false) } catch {}
    }
    if ($word) {
        try { $word.Quit() } catch {}
    }
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
}

Write-Host "=== 完成 ===" -ForegroundColor Cyan

# Ensure output dir
$outputDir = "C:\Users\ASDCF\.qclaw\workspace"
$outputPdf = Join-Path $outputDir "新丝路跨境_实战出海_第二套商业模式方案书.pdf"

# Launch Word
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = $false

try {
    $docPath = "C:\Users\ASDCF\Desktop\新丝路跨境_实战出海_第二套商业模式方案书.docx"
    Write-Host "Opening document..."
    $doc = $word.Documents.Open($docPath)
    
    # Set page to A4
    $doc.PageSetup.PageWidth = [float]595.35  # A4 in points
    $doc.PageSetup.PageHeight = [float]841.95
    $doc.PageSetup.TopMargin = [float]72    # 1 inch
    $doc.PageSetup.BottomMargin = [float]72
    $doc.PageSetup.LeftMargin = [float]90   # 1.25 inch
    $doc.PageSetup.RightMargin = [float]90
    
    Write-Host "Applying professional styles..."
    
    # Apply professional formatting to all paragraphs
    # Set default font
    $doc.Content.Font.Name = "Calibri"
    $doc.Content.Font.Size = 11
    $doc.Content.ParagraphFormat.LineSpacing = [int]15  # 1.15 line spacing
    
    # Process each paragraph
    $paraCount = $doc.Paragraphs.Count
    Write-Host "Processing $paraCount paragraphs..."
    
    # Track headings for TOC-like visual hierarchy
    for ($i = 1; $i -le $paraCount; $i++) {
        $para = $doc.Paragraphs.Item($i)
        $range = $para.Range
        $text = $range.Text.Trim()
        if ([string]::IsNullOrEmpty($text)) { continue }
        
        # Detect heading level by content
        if ($text -match '^[一二三四五六七八九十]+、') {
            # Level 1 headings: 一、二、三 etc
            # Heading 1 style - already applied? Let's check
            Write-Host "H1: $($text.Substring(0, [Math]::Min(30, $text.Length)))"
        } elseif ($text -match '^\d+\.\d+ ') {
            # Level 2 headings: 1.1, 1.2 etc
        } elseif ($text -match '^\d+\.\d+\.\d+ ') {
            # Level 3 headings: 1.1.1 etc
        }
    }
    
    # Add a professional cover page (as first section)
    Write-Host "Adding cover page..."
    
    # Actually, let's modify the existing content to be more professional
    # rather than adding new pages
    
    # Add header with company name
    $section = $doc.Sections.Item(1)
    
    # Footer with page numbers
    $footer = $section.Footers.Item(1)  # wdHeaderFooterPrimary = 1
    $footer.LinkToPrevious = $false
    $footerRange = $footer.Range
    $footerRange.Text = ""
    $footerRange.ParagraphFormat.Alignment = 1  # wdAlignParagraphCenter = 1
    
    # Add page number
    $footerRange.Text = "- "
    $footerRange.Collapse(0)  # wdCollapseEnd
    $footerRange.Fields.Add($footerRange, -1, "PAGE", $false)  # wdFieldPage = -1
    $footerRange.Collapse(0)
    $footerRange.Text = " -"
    
    # Set footer font
    $footerRange.Font.Name = "Calibri"
    $footerRange.Font.Size = 9
    $footerRange.Font.Color = [int]12632256  # Gray
    
    # Header
    $header = $section.Headers.Item(1)  # wdHeaderFooterPrimary = 1
    $header.LinkToPrevious = $false
    $headerRange = $header.Range
    $headerRange.Text = "新丝路跨境 · 实战出海 · 商业模式方案书"
    $headerRange.Font.Name = "Calibri"
    $headerRange.Font.Size = 9
    $headerRange.Font.Italic = 1  # $true
    $headerRange.Font.Color = [int]10066329  # Dark gray
    $headerRange.ParagraphFormat.Alignment = 0  # wdAlignParagraphLeft
    
    # Save as PDF with high quality
    Write-Host "Exporting to PDF..."
    # wdExportFormatPDF = 17
    $doc.ExportAsFixedFormat($outputPdf, 17, $false, 0, [ref]0, [ref]0, [ref]0, [ref]0, [ref]$false)
    
    $doc.Close()
    Write-Host "PDF created: $outputPdf"
}
catch {
    Write-Host "ERROR: $_"
}
finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
}

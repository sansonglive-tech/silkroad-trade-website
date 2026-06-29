$file = "C:\Users\ASDCF\.qclaw\workspace\silkroad-trade_v7_silk_poster.html"
$content = [System.IO.File]::ReadAllText($file)

$scriptIdx = $content.IndexOf("<script>")
if ($scriptIdx -lt 0) {
    Write-Host "ERROR: No script tag found!"
    exit 1
}

Write-Host "script at: $scriptIdx"

# Show next 100 chars
$afterScript = $content.Substring($scriptIdx, 100)
Write-Host "After script tag:"
$afterScript.ToCharArray() | ForEach-Object { Write-Host "$( [int][char]$_ ) '$_'" }

# Check what's between </style> and <script> to see if the script was consumed
$styleIdx = $content.LastIndexOf("</style>")
$gap = $content.Substring($styleIdx, 60)
Write-Host "`nBetween </style> and next:"
$gap.ToCharArray() | ForEach-Object { Write-Host "$( [int][char]$_ ) '$_'" }

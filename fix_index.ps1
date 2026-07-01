# Fix index.html encoding
$v7 = Get-Content "$PSScriptRoot\silkroad-trade_v7_silk_poster.html" -Raw -Encoding UTF8
$cfg = Get-Content "$PSScriptRoot\site_config.json" -Raw -Encoding UTF8

# Replace CONFIG
$marker = 'const CONFIG = '
$idx = $v7.IndexOf($marker)
$braceIdx = $v7.IndexOf('{', $idx)
$depth = 0
$end = $braceIdx
for ($i = $braceIdx; $i -lt $v7.Length; $i++) {
    if ($v7[$i] -eq '{') { $depth++ }
    elseif ($v7[$i] -eq '}') { $depth-- }
    if ($depth -eq 0) { $end = $i + 1; break }
}

$newHtml = $v7.Substring(0, $idx) + "const CONFIG = $cfg;" + $v7.Substring($end)

# Write with UTF8 BOM
$utf8Bom = New-Object System.Text.UTF8Encoding $true
[System.IO.File]::WriteAllText("$PSScriptRoot\index.html", $newHtml, $utf8Bom)

Write-Host "Done"

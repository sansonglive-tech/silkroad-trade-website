$t = [Math]::Floor([DateTimeOffset]::Now.ToUnixTimeSeconds())
$from = $t - 604800
Write-Output $from
Write-Output $t

$t = [Math]::Floor([DateTimeOffset]::Now.ToUnixTimeSeconds())
$from = $t - 604800
$result = @{
    from_time = $from
    to_time = $t
}
$resultJson = $result | ConvertTo-Json -Compress
node 'E:\腾讯龙虾\QClaw\resources\openclaw\config\skills\online-search\scripts\prosearch.cjs' $resultJson

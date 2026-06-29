$t = [Math]::Floor([DateTimeOffset]::Now.ToUnixTimeSeconds())
$from = $t - 604800
$json = "{`"keyword`":`"C罗最新消息`",`"from_time`":$from,`"to_time`":$t}"
node 'E:\腾讯龙虾\QClaw\resources\openclaw\config\skills\online-search\scripts\prosearch.cjs' $json

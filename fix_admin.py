with open(r"C:\Users\ASDCF\.qclaw\workspace\admin_server.py", "r", encoding="utf-8") as f:
    c = f.read()

# Fix f-string backslash issue (Python 3.11 doesn't support backslash in f-string expression)
c = c.replace(
    "print(f\"  v7 状态: {'\\u2705' if v7_ok else '\\u274c'}\")",
    "print('  v7 状态: ' + ('\u2705' if v7_ok else '\u274c'))"
)
c = c.replace(
    "print(f\"  v6 状态: {'\\u2705' if v6_ok else '\\u274c'}\")",
    "print('  v6 状态: ' + ('\u2705' if v6_ok else '\u274c'))"
)
c = c.replace(
    "print(f\"  \u26a0\ufe0f 不改 v7 代码，配置存在 site_config.json\\n\")",
    "print('  \u26a0\ufe0f 不改 v7 代码，配置存在 site_config.json\\n')"
)

with open(r"C:\Users\ASDCF\.qclaw\workspace\admin_server.py", "w", encoding="utf-8") as f:
    f.write(c)
print("Fixed f-string backslash issues")

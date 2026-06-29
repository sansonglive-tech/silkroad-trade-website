import sys, re, json
sys.stdout.reconfigure(encoding="utf-8")

with open(r"C:\Users\ASDCF\.qclaw\workspace\silkroad-trade_v7_silk_poster.html", "r", encoding="utf-8") as f:
    html = f.read()

# Find CONFIG = { ... };
# Strategy: find all CONFIG occurrences and their approach
for m in re.finditer(r"const\s+CONFIG\s*=\s*(\{[^;]+?\});", html, re.DOTALL):
    start = m.start()
    end = m.end()
    print(f"CONFIG at {start}-{end} ({end-start} bytes)")
    # Show first/last 100 chars
    print("  FIRST:", m.group(1)[:100].replace("\n"," "))
    print("  LAST:", m.group(1)[-100:].replace("\n"," "))
    print()

# Also check for CONFIG usage
for m in re.finditer(r"CONFIG\.\w+", html):
    print(f"Usage: {m.group()} at {m.start()}")
    break # just first few

# Count total CONFIG refs
print(f"\nTotal CONFIG references: {len(re.findall(r'CONFIG', html))}")

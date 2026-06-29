import json, re

cfg = json.load(open(r"C:\Users\ASDCF\.qclaw\workspace\site_config.json", "r", encoding="utf-8"))

def to_js(val, indent=0):
    pad = "  " * indent
    if val is None: return "null"
    if isinstance(val, bool): return "true" if val else "false"
    if isinstance(val, (int, float)): return str(val)
    if isinstance(val, str):
        escaped = val.replace("\\", "\\\\").replace("'", "\\'")
        return "'" + escaped + "'"
    if isinstance(val, dict):
        items = []
        for k, v in val.items():
            items.append(pad + "    " + k + ": " + to_js(v, indent+1))
        return "{\n" + ",\n".join(items) + "\n" + pad + "  }"
    if isinstance(val, list):
        items = [pad + "    " + to_js(v, indent+1) for v in val]
        return "[\n" + ",\n".join(items) + "\n" + pad + "  ]"
    return "null"

js = to_js(cfg)
print("=== TOP ===")
print(js[:300])
print("\n=== BOTTOM ===")
print(js[-300:])
print("\n=== LENGTH ===", len(js))

with open(r"C:\Users\ASDCF\.qclaw\workspace\silkroad-trade_v7_silk_poster.html", "r", encoding="utf-8") as f:
    html = f.read()

m = re.search(r"const\s+CONFIG\s*=\s*\{[^;]+?\};", html)
if m:
    print("\n=== MATCH ===")
    print("FIRST:", m.group()[:100])
    print("LAST:", m.group()[-100:])
    # Test replacement
    new_html = html[:m.start()] + "const CONFIG = " + js + ";" + html[m.end():]
    print("REPLACED length:", len(new_html), "(was", len(html), ")")
    # Verify no CONFIG refs broken
    print("CONFIG refs:", len(re.findall(r"CONFIG\.\w+", new_html)))
    # Verify no JS syntax break
    if "const CONFIG = " in new_html:
        print("REPLACEMENT OK")
    # Check for any { or } imbalance
    opens = new_html.count("{")
    closes = new_html.count("}")
    print("Braces: {", opens, "} ", closes, " diff:", opens-closes)
else:
    print("\n=== NO MATCH ===")

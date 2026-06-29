import re
with open("C:/Users/ASDCF/.qclaw/workspace/preview_test.html", "r", encoding="utf-8") as f:
    d = f.read()

# Show the full CONFIG after injection
m = re.search(r"const CONFIG = (\{.+?\});", d, re.DOTALL)
if m:
    cfg_text = m.group(1)
    print(cfg_text[:500])
    print("\n...")
    print(cfg_text[-500:])

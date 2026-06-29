import re
with open("C:/Users/ASDCF/.qclaw/workspace/silkroad-trade_v7_silk_poster.html", "r", encoding="utf-8") as f:
    html = f.read()

# Find each section's inner content
pairs = [
    ("services", r'(<div class="services-grid">)(.*?)(</div>\s*\n\s*</section>)', re.DOTALL),
    ("stats", r'(<div class="stats-inner">)(.*?)(</div>\s*\n\s*</section>)', re.DOTALL),
    ("policies", r'(<div class="policy-grid">)(.*?)(</div>\s*\n\s*</section>)', re.DOTALL),
    ("testimonials", r'(<div class="testimonials-grid">)(.*?)(</div>\s*\n\s*</section>)', re.DOTALL),
    ("process", r'(<div class="process-grid">)(.*?)(</div>\s*\n\s*</section>)', re.DOTALL),
]

for name, pat, flags in pairs:
    m = re.search(pat, html, flags)
    if m:
        inner = m.group(2)
        # Trim whitespace
        inner_stripped = inner.strip()
        print(f"[{name}] start={m.start(2)}, end={m.end(2)}, len={len(inner)}")
        print(f"  before: {repr(m.group(1)[:60])}")
        print(f"  content preview: {inner[:80]}...")
        print(f"  after: {repr(m.group(3)[:60])}")
        print()
    else:
        print(f"[{name}] NOT FOUND")

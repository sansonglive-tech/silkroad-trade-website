import sys, re, traceback
sys.stdout.reconfigure(encoding="utf-8")

with open(r"C:\Users\ASDCF\.qclaw\workspace\silkroad-trade_v7_silk_poster.html", encoding="utf-8") as f:
    html = f.read()

def rg(pat, text, default=""):
    m = re.search(pat, text)
    return m.group(1) if m else default

# Test step by step
try:
    # 1. company
    for k in ["name", "slogan", "email", "icp", "wechatId", "wechatQR"]:
        v = rg(r"\b" + k + r":\s*'([^']*)'", html, "")
        print(f"company.{k}: {v[:50] if v else '(empty)'}")
    print("STEP 1 OK")
    
    # 2. slides
    m = re.search(r"const\s+SLIDE_CONFIG\s*=\s*\[(.*?)\];", html, re.DOTALL)
    if m:
        objs = re.findall(r"\{([^}]+)\}", m.group(1), re.DOTALL)
        print(f"slides: {len(objs)} items")
        for obj in objs[:2]:
            t = re.sub(r"<[^>]+>", "", rg(r"'title':\s*'([^']*)'", obj, ""))
            print(f"  title={t[:30]}")
    else:
        print("slides: NOT FOUND")
    print("STEP 2 OK")
    
    # 3. services
    sidx = html.find('id="services"')
    if sidx >= 0:
        sec_end = html.find("</section>", sidx)
        print(f"services section: {sec_end-sidx} chars")
    else:
        print("services: NOT FOUND")
    print("STEP 3 OK")
    
    # 4. stats - use html.find to avoid regex issues
    sb_idx = html.find('stats-banner')
    if sb_idx >= 0:
        sec_start = html.rfind("<section", 0, sb_idx)
        if sec_start >= 0:
            sec_end = html.find("</section>", sb_idx)
            if sec_end >= 0:
                sec_html = html[sec_start:sec_end+10]
                im = re.search(r'<div class="stats-inner">(.*?)</div>', sec_html, re.DOTALL)
                if im:
                    nums = re.findall(r'<div class="num">([^<]+)<', im.group(1))
                    print(f"stats: {len(nums)} items, nums={nums}")
                else:
                    print("stats: inner NOT FOUND")
            else:
                print("stats: sec_end NOT FOUND")
        else:
            print("stats: section start NOT FOUND")
    else:
        print("stats: banner NOT FOUND")
    print("STEP 4 OK")
    
    print("\n==== ALL STEPS PASSED ====")
    
except Exception as e:
    traceback.print_exc()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Fix: move /api/book (POST) and /api/bookings (GET) BEFORE login check

FILE = r"C:\Users\ASDCF\.qclaw\workspace\admin_server.py"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

# === do_POST: move /api/book before login check ===
# Current: old block with /api/book AFTER the login check
old_post_book = '''        if p == "/api/trace_clear":
                TRACE_LOG.clear()
                self.rjson({"success": True})
            elif p == "/api/book":
                n = int(self.headers.get("Content-Length", 0))
                data = json.loads(self.rfile.read(n).decode("utf-8"))
                from datetime import datetime
                data["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                BOOKING_COUNTER[0] += 1
                data["id"] = BOOKING_COUNTER[0]
                bookings = load_bookings()
                bookings.append(data)
                save_bookings(bookings)
                self.rjson({"success": True, "message": "\u9884\u7ea6\u5df2\u63d0\u4ea4"})
                return
            if p == "/api/bookings":
                self.rjson(load_bookings())
            elif '''

# New: put /api/book + /api/bookings BEFORE the login check line
new_post_book = '''        if p == "/api/trace_clear":
                TRACE_LOG.clear()
                self.rjson({"success": True})
            elif p == "/api/book":
                n = int(self.headers.get("Content-Length", 0))
                data = json.loads(self.rfile.read(n).decode("utf-8"))
                from datetime import datetime
                data["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                BOOKING_COUNTER[0] += 1
                data["id"] = BOOKING_COUNTER[0]
                bookings = load_bookings()
                bookings.append(data)
                save_bookings(bookings)
                self.rjson({"success": True, "message": "\u9884\u7ea6\u5df2\u63d0\u4ea4"})
                return
            elif '''

# The login check line we need to find for do_GET:
# Need to add /api/bookings BEFORE the do_GET login check
login_get_marker = '''# 以下路由需要登录
            tok = self.get_session()
            if not tok:
                self.redirect("/login")
                return'''
new_get_section = '''        if p == "/api/bookings":
                self.rjson(load_bookings())
            # 以下路由需要登录
            tok = self.get_session()
            if not tok:
                self.redirect("/login")
                return'''

if old_post_book in content:
    content = content.replace(old_post_book, new_post_book, 1)
    print("✅ do_POST: /api/book 已移到登录检查之前")
else:
    print("❌ do_POST: 未找到 /api/book 位置")

if login_get_marker in content:
    content = content.replace(login_get_marker, new_get_section, 1)
    print("✅ do_GET: /api/bookings 已移到登录检查之前")
else:
    print("❌ do_GET: 未找到登录检查标记")
    idx = content.find("以下路由需要登录", content.find("def do_GET"))
    print(f"   位置 {idx}: {repr(content[idx-50:idx+100])}")

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print("\n🎉 修复完成！")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
丝路山海通 预约记录服务
===============================
完全独立运行，不修改任何现有文件。
端口: 8081 | 数据: booking_data.json
"""

import http.server
import json
import os
from datetime import datetime
from urllib.parse import urlparse

PORT = 8081
WORKSPACE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(WORKSPACE, "booking_data.json")

# 数据层
def load_bookings():
    if os.path.isfile(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_bookings(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 后台管理页面 HTML (从外部文件加载)
ADMIN_HTML = None

def get_admin_html():
    global ADMIN_HTML
    if ADMIN_HTML:
        return ADMIN_HTML
    
    html_path = os.path.join(WORKSPACE, "booking_admin.html")
    if os.path.isfile(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            ADMIN_HTML = f.read()
    else:
        ADMIN_HTML = "<h1>booking_admin.html not found</h1>"
    return ADMIN_HTML

# 前端 Hook JS
HOOK_JS = r"""
(function(){
var BOOKING_SERVER='http://localhost:8081';
window.submitBook=function(){
var name=(document.getElementById('bookName')||{}).value;
var phone=(document.getElementById('bookPhone')||{}).value;
var country=(document.getElementById('bookCountry')||{}).value;
if(!name||!name.trim()||!phone||!phone.trim()){alert('\u8bf7\u586b\u5199\u59d3\u540d\u548c\u624b\u673a\u53f7\u7801');return;}
var x=new XMLHttpRequest();
x.open('POST',BOOKING_SERVER+'/api/booking',true);
x.setRequestHeader('Content-Type','application/json');
x.onload=function(){
if(x.status===200){
alert('\u2705 \u9884\u7ea6\u63d0\u4ea4\u6210\u529f\uff01\u6211\u4eec\u5c06\u5c3d\u5feb\u4e0e\u60a8\u8054\u7cfb\u3002');
var nm=document.getElementById('bookName');if(nm)nm.value='';
var ph=document.getElementById('bookPhone');if(ph)ph.value='';
var ct=document.getElementById('bookCountry');if(ct)ct.value='';
if(typeof closeBook==='function')closeBook();
}else{alert('\u274c \u63d0\u4ea4\u5931\u8d25\uff0c\u8bf7\u7a0d\u540e\u91cd\u8bd5');}
};
x.onerror=function(){alert('\u274c \u7f51\u7edc\u9519\u8bef\uff0c\u8bf7\u786e\u8ba4\u9884\u7ea6\u670d\u52a1\u5df2\u542f\u52a8\uff08\u7aef\u53e38081\uff09');};
x.send(JSON.stringify({name:name.trim(),phone:phone.trim(),country:(country||'').trim()}));
};
console.log('[Booking Hook] enabled -> '+BOOKING_SERVER);
})();
"""

class Handler(http.server.BaseHTTPRequestHandler):
    
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == "/admin" or path == "/admin/":
            self._html(get_admin_html())
        elif path == "/booking_hook.js":
            self._send(200, HOOK_JS, "application/javascript; charset=utf-8")
        elif path == "/api/bookings":
            data = load_bookings()
            data.reverse()
            self._json(data)
        elif path == "/api/stats":
            data = load_bookings()
            today = datetime.now().strftime("%Y-%m-%d")
            self._json({
                "total": len(data),
                "today": sum(1 for b in data if b.get("created_at","").startswith(today)),
                "pending": sum(1 for b in data if b.get("status") != "done")
            })
        elif path == "/status" or path == "/":
            self._json({
                "service": "silkroad-booking-server",
                "status": "running",
                "port": PORT,
                "admin": "http://localhost:%d/admin" % PORT,
                "bookings": len(load_bookings())
            })
        else:
            self._json({"error": "not found"}, 404)
    
    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        
        try:
            data = json.loads(body)
        except:
            self._json({"error": "invalid JSON"}, 400)
            return
        
        if path == "/api/booking":
            name = (data.get("name") or "").strip()
            phone = (data.get("phone") or "").strip()
            country = (data.get("country") or "").strip()
            if not name or not phone:
                self._json({"error": "name and phone required"}, 400)
                return
            record = {
                "id": int(datetime.now().timestamp() * 1000),
                "name": name,
                "phone": phone,
                "country": country,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "new"
            }
            bookings = load_bookings()
            bookings.append(record)
            save_bookings(bookings)
            self._json({"success": True, "id": record["id"]})
            
        elif path == "/api/booking/update":
            bid = data.get("id")
            status = data.get("status", "done")
            bookings = load_bookings()
            for b in bookings:
                if b.get("id") == bid:
                    b["status"] = status
                    b["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    break
            save_bookings(bookings)
            self._json({"success": True})
            
        elif path == "/api/booking/delete":
            bid = data.get("id")
            bookings = load_bookings()
            before = len(bookings)
            bookings = [b for b in bookings if b.get("id") != bid]
            if len(bookings) < before:
                save_bookings(bookings)
            self._json({"success": True})
        else:
            self._json({"error": "not found"}, 404)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    
    def _html(self, content):
        self._send(200, content, "text/html; charset=utf-8")
    
    def _json(self, obj, code=200):
        self._send(code, json.dumps(obj, ensure_ascii=False), "application/json; charset=utf-8")
    
    def _send(self, code, body, ctype):
        self.send_response(code)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", len(body.encode("utf-8")))
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))
    
    def log_message(self, fmt, *args):
        ts = datetime.now().strftime("%H:%M:%S")
        print("  [%s] %s %s -> %s" % (ts, args[0], args[1], args[2]))


if __name__ == "__main__":
    print()
    print("  +----------------------------------------+")
    print("  |   Silkroad Booking Service             |")
    print("  |   Independent - no files modified      |")
    print("  +----------------------------------------+")
    print()
    print("  >> Admin:   http://localhost:%d/admin" % PORT)
    print("  >> Submit:  http://localhost:%d/api/booking" % PORT)
    print("  >> Hook:    http://localhost:%d/booking_hook.js" % PORT)
    print("  >> Data:    %s" % DATA_FILE)
    print("  >> Bookings: %d" % len(load_bookings()))
    print()
    
    server = http.server.HTTPServer(("0.0.0.0", PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Stopped.")
        server.server_close()

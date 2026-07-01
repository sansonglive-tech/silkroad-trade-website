#!/usr/bin/env python3
# 直接测试后端发布 API
import urllib.request
import json

# 先用登录获取 token
login_data = json.dumps({"username": "jackleework", "password": "999999"}).encode('utf-8')
req = urllib.request.Request(
    'http://localhost:8080/api/login',
    data=login_data,
    headers={'Content-Type': 'application/json'},
    method='POST'
)

try:
    response = urllib.request.urlopen(req, timeout=5)
    cookie = response.headers.get('Set-Cookie', '')
    print("登录成功")
    
    # 测试发布
    req2 = urllib.request.Request(
        'http://localhost:8080/api/publish',
        data='{}'.encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'Cookie': cookie
        },
        method='POST'
    )
    response2 = urllib.request.urlopen(req2, timeout=60)
    result = json.loads(response2.read().decode('utf-8'))
    print(f"发布结果: {result}")
    
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code}")
    print(e.read().decode('utf-8')[:300])
except Exception as e:
    print(f"Error: {str(e)[:200]}")

#!/usr/bin/env python3
import urllib.request
import urllib.parse
import json

# 1. 登录获取 cookie
login_data = json.dumps({"username": "jackleework", "password": "999999"}).encode('utf-8')
req = urllib.request.Request(
    'http://localhost:8080/api/login',
    data=login_data,
    headers={'Content-Type': 'application/json'},
    method='POST'
)

try:
    response = urllib.request.urlopen(req, timeout=5)
    # 获取 cookie
    cookie = response.headers.get('Set-Cookie', '')
    print('Cookie:', cookie[:100])
    
    # 2. 用 cookie 访问 admin
    req2 = urllib.request.Request(
        'http://localhost:8080/admin',
        headers={'Cookie': cookie}
    )
    response2 = urllib.request.urlopen(req2, timeout=5)
    data = response2.read().decode('utf-8')
    
    # 检查 LB
    idx = data.find('var LB=')
    if idx >= 0:
        end = data.find(';', idx)
        lb = data[idx:end+1]
        print('LB:', lb)
    else:
        print('No LB found')
    
    # 检查中文
    if '公司名称' in data:
        print('Has 公司名称: YES')
    else:
        print('Has 公司名称: NO')
        with open('_admin.html', 'w', encoding='utf-8') as f:
            f.write(data)
        print('Saved to _admin.html')
        
except Exception as e:
    print('Error:', e)

#!/usr/bin/env python3
import urllib.request
import urllib.error

# 测试 /admin 页面（需要登录，会被重定向到登录页）
print("=== 测试 /admin (无 Cookie) ===")
try:
    req = urllib.request.Request('http://localhost:8080/admin')
    response = urllib.request.urlopen(req, timeout=5)
    print('Status:', response.status)
    data = response.read().decode('utf-8')
    print('Length:', len(data))
    if '500' in data or 'Error' in data:
        print('Content preview:', data[:500])
except urllib.error.HTTPError as e:
    print('HTTP Error:', e.code)
    print('Response:', e.read().decode('utf-8')[:500])
except Exception as e:
    print('Error:', e)

# 测试 /api/config
print("\n=== 测试 /api/config ===")
try:
    req = urllib.request.Request('http://localhost:8080/api/config')
    response = urllib.request.urlopen(req, timeout=5)
    print('Status:', response.status)
    data = response.read().decode('utf-8')
    print('Length:', len(data))
    print('First 200 chars:', data[:200])
except Exception as e:
    print('Error:', e)

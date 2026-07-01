#!/usr/bin/env python3
import urllib.request
import urllib.error

try:
    req = urllib.request.Request('http://localhost:8080/admin')
    req.add_header('Cookie', 'admin_token=test')
    response = urllib.request.urlopen(req, timeout=5)
    print('Status:', response.status)
    data = response.read().decode('utf-8')
    print('Length:', len(data))
except urllib.error.HTTPError as e:
    print('HTTP Error:', e.code)
    print('Response:', e.read().decode('utf-8')[:500])
except Exception as e:
    print('Error:', e)

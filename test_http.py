#!/usr/bin/env python3
import urllib.request

try:
    response = urllib.request.urlopen('http://localhost:8080/admin', timeout=5)
    data = response.read().decode('utf-8')
    
    # 找到 LB
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
        # 保存检查
        with open('_response.html', 'w', encoding='utf-8') as f:
            f.write(data)
        print('Saved to _response.html')
        
except Exception as e:
    print('Error:', e)

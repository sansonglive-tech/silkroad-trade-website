#!/usr/bin/env python3
import json

with open('site_config.json', 'r', encoding='utf-8') as f:
    cfg = json.load(f)

print("公司名:", cfg['company']['name'])
print("邮箱:", cfg['company']['email'])
print("ICP:", cfg['company']['icp'])
print("政策数:", len(cfg['policies']))
print("服务流程数:", len(cfg['process']))
print("客户案例数:", len(cfg['testimonials']))

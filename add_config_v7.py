#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""在 v7 中添加 CONFIG 配置区（不改 v6）"""
import re, os, shutil

V7 = "C:/Users/ASDCF/.qclaw/workspace/silkroad-trade_v7_silk_poster.html"
V6 = "C:/Users/ASDCF/.qclaw/workspace/silkroad-trade_v6_silk_poster.html"

# 如果 v7 坏了，从 v6 恢复
if not os.path.isfile(V7) or os.path.getsize(V7) < 1000:
    print("[安全] v7 异常，从 v6 恢复...")
    shutil.copy2(V6, V7)

with open(V7, "r", encoding="utf-8") as f:
    html = f.read()

# 检查是否已有 CONFIG
if "const CONFIG" in html:
    print("CONFIG 已存在，跳过添加")
    exit(0)

# 在第一个 <script> 后插入
pos = html.find("<script>") + len("<script>")

config_block = """

// >>> 配置区 — 在这里修改所有内容和图片 <<<
// ================================================================

const CONFIG = {

  // === 公司信息 ===
  company: {
    name: '丝路山海通',
    slogan: '一带一路企业出海一站式服务',
    email: 'outlook@silkroad-trade.com',
    icp: '粤ICP备XXXXXXXX号',
    wechatId: 'SilkRoadTrade',
    wechatQR: 'wechat/二维码.jpg',
  },

  // === 统计数字 ===
  stats: [
    { num: '60+', label: '一带一路覆盖国家' },
    { num: '1,600+', label: '服务出海企业' },
    { num: '400+', label: '海外本地员工' },
    { num: '5+', label: '区域服务网络' },
  ],

  // === 轮播图 ===
  slides: [
    { id: 'slide-1', title: '乘丝路长风<span class="gold">通达全球</span>', subtitle: '一带一路企业出海一站式服务', desc: '丝路山海通 — 响应国家一带一路倡议，为企业出海提供公司注册、财税支持、产品准入、本地化运营等一站式落地服务。', img: 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&q=80&auto=format', detailId: 'company-advantage' },
    { id: 'slide-2', title: '公司注册<span class="gold">资质办理</span>', subtitle: '最快7个工作日完成海外公司设立', desc: '境内境外公司注册、营业执照激活、行业资质证照办理，让您的企业快速合法落地海外。', img: 'https://images.unsplash.com/photo-1560179707-f14e90ef3623?w=800&q=80&auto=format', detailId: 'company-reg' },
    { id: 'slide-3', title: '财税人事<span class="gold">法务合规</span>', subtitle: '本地化运营全方位保障', desc: '财税筹划、代理记账、人事雇佣、法务咨询、合规审计，专业团队为您保驾护航。', img: 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800&q=80&auto=format', detailId: 'tax-legal' },
    { id: 'slide-4', title: '产品准入<span class="gold">认证通关</span>', subtitle: 'SNI/BPOM/清真认证一站式办理', desc: 'SNI认证、BPOM注册、清真认证、进出口许可证、海关备案等全套产品合规准入服务。', img: 'https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=800&q=80&auto=format', detailId: 'certification' },
    { id: 'slide-5', title: '本地运营<span class="gold">长期陪伴</span>', subtitle: '真正扎根海外市场', desc: '行政办公、本地招聘、政府关系、行业资源对接、展会活动策划，让您出海无忧。', img: 'https://images.unsplash.com/photo-1521737711867-e3b97375f902?w=800&q=80&auto=format', detailId: 'local-ops' },
    { id: 'slide-6', title: '签证考察<span class="gold">商务出行</span>', subtitle: '签证办理与商务考察一站式', desc: '商务签证、工作签证、工厂考察、市场调研、政府对接，一站式行程安排，助您轻松出海考察。', img: 'https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=800&q=80&auto=format', detailId: 'visa' },
    { id: 'slide-7', title: '建厂工程<span class="gold">落地投产</span>', subtitle: '海外建厂与基建全流程服务', desc: '海外选址建厂、建筑工程许可、环境合规、能源矿产、IT通讯等基建配套，让您的工厂快速落地。', img: 'https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?w=800&q=80&auto=format', detailId: 'factory' },
  ],

};

// ================================================================

"""

new_html = html[:pos] + config_block + html[pos:]

# 先写临时文件再替换（原子操作，防损坏）
tmp = V7 + ".tmp"
with open(tmp, "w", encoding="utf-8") as f:
    f.write(new_html)
os.replace(tmp, V7)

print(f"✅ CONFIG 已添加到 v7（{len(new_html)} 字节）")
print("✅ v6 不动")

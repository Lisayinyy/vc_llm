#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
国内 12 家头部大模型公司 - 数据落盘
源数据：2026-07-13 / 2026-07-14 企查查 API 调用结果
"""

import json
from pathlib import Path

OUT = Path("/workspace/llm-graph")
OUT.mkdir(parents=True, exist_ok=True)

# ===== 12 家公司工商信息（已从企查查拉到） =====
companies = [
    {
        "name": "北京智谱华章科技股份有限公司",
        "short": "智谱",
        "uscc": "91110108MA01KP2T5U",
        "legal_rep": "刘德兵",
        "register_capital_wan": 4458.4309,
        "establish_date": "2019-06-11",
        "location": "北京",
        "listing": "上市(港股)",
        "industry": "通用大模型 GLM",
        "employee_count": 789,
        "company_type": "股份有限公司（外商投资、上市）",
    },
    {
        "name": "北京月之暗面科技有限公司",
        "short": "月之暗面",
        "uscc": "91110108MACG2KBH8F",
        "legal_rep": "杨植麟",
        "register_capital_wan": 152.3585,
        "establish_date": "2023-04-17",
        "location": "北京",
        "listing": "未上市(独角兽)",
        "industry": "Kimi 长文本大模型",
        "employee_count": 233,
        "company_type": "有限责任公司（自然人投资或控股）",
    },
    {
        "name": "百川智能科技有限公司",
        "short": "百川智能",
        "uscc": "91110108MACBM7E07B",
        "legal_rep": "王小川",
        "register_capital_wan": 647.6684,
        "establish_date": "2023-03-24",
        "location": "北京",
        "listing": "未上市",
        "industry": "百川大模型 (医疗方向)",
        "employee_count": 200,
        "company_type": "有限责任公司（自然人投资或控股）",
    },
    {
        "name": "上海稀宇极智科技有限公司",
        "short": "MiniMax",
        "uscc": "91310000MA7CGN828C",
        "legal_rep": "闫俊杰",
        "register_capital_wan": 400000.0,
        "establish_date": "2021-11-03",
        "location": "上海",
        "listing": "未上市(独角兽)",
        "industry": "MiniMax 海螺 AI / Talkie",
        "employee_count": 269,
        "company_type": "有限责任公司（港澳台法人独资）",
    },
    {
        "name": "北京零一万物科技有限公司",
        "short": "零一万物",
        "uscc": "91110108MACGNQDM2B",
        "legal_rep": "马杰",
        "register_capital_wan": 10000.0,
        "establish_date": "2023-05-16",
        "location": "北京",
        "listing": "未上市",
        "industry": "Yi 大模型 (李开复系)",
        "employee_count": 0,
        "company_type": "有限责任公司（外商投资企业法人独资）",
    },
    {
        "name": "上海阶跃星辰智能科技股份有限公司",
        "short": "阶跃星辰",
        "uscc": "91310104MACE0YX639",
        "legal_rep": "印奇",
        "register_capital_wan": 6657.6028,
        "establish_date": "2023-04-06",
        "location": "上海",
        "listing": "未上市(独角兽)",
        "industry": "Step 大模型 (印奇/旷视系)",
        "employee_count": 214,
        "company_type": "股份有限公司（港澳台投资、未上市）",
    },
    {
        "name": "北京生数科技股份有限公司",
        "short": "生数科技",
        "uscc": "91110108MACC4D63XF",
        "legal_rep": "鲍凡",
        "register_capital_wan": 1701.0235,
        "establish_date": "2023-03-06",
        "location": "北京",
        "listing": "未上市",
        "industry": "Vidu 视频生成大模型 (清华系)",
        "employee_count": 119,
        "company_type": "股份有限公司（港澳台投资、未上市）",
    },
    {
        "name": "杭州深度求索人工智能基础技术研究有限公司",
        "short": "深度求索",
        "uscc": "91330105MACPN4X08Y",
        "legal_rep": "裴湉",
        "register_capital_wan": 1500.0,
        "establish_date": "2023-07-17",
        "location": "杭州",
        "listing": "未上市(独角兽)",
        "industry": "DeepSeek 通用大模型 (幻方系)",
        "employee_count": 46,
        "company_type": "其他有限责任公司",
    },
    {
        "name": "北京面壁智能科技有限责任公司",
        "short": "面壁智能",
        "uscc": "91110108MABU8XJRXD",
        "legal_rep": "曾国洋",
        "register_capital_wan": 77.29165,
        "establish_date": "2022-08-12",
        "location": "北京",
        "listing": "未上市",
        "industry": "CPM/ModelForce 大模型 (清华系)",
        "employee_count": 205,
        "company_type": "有限责任公司（港澳台投资、非独资）",
    },
    {
        "name": "北京衔远科技有限公司",
        "short": "衔远科技",
        "uscc": "91110105MA04GN5E7L",
        "legal_rep": "周怡文",
        "register_capital_wan": 500.0,
        "establish_date": "2021-10-29",
        "location": "北京",
        "listing": "未上市",
        "industry": "圆桌大模型 (周伯文/京东系)",
        "employee_count": 32,
        "company_type": "有限责任公司（自然人独资）",
    },
    {
        "name": "上海无问芯穹智能科技股份有限公司",
        "short": "无问芯穹",
        "uscc": "91310104MACJB73JXU",
        "legal_rep": "李玉晨",
        "register_capital_wan": 271.1934,
        "establish_date": "2023-05-31",
        "location": "上海",
        "listing": "未上市",
        "industry": "端侧大模型 / 算力 (清华系)",
        "employee_count": 99,
        "company_type": "股份有限公司（港澳台投资、未上市）",
    },
    {
        "name": "北京瑞莱智慧科技有限公司",
        "short": "瑞莱智慧",
        "uscc": "91110108MA01DNC75B",
        "legal_rep": "田天",
        "register_capital_wan": 1236.2761,
        "establish_date": "2018-07-25",
        "location": "北京",
        "listing": "未上市",
        "industry": "RealAI 安全大模型 (清华系)",
        "employee_count": 100,
        "company_type": "其他有限责任公司",
    },
]

# ===== 已拉到的股东数据 =====
shareholders = {
    "智谱": [
        {"name": "北京链湃科技发展中心（有限合伙）", "type": "legal", "ratio": 7.63, "note": "创始团队持股平台"},
        {"name": "珠海横琴慧惠企业管理合伙企业（有限合伙）", "type": "legal", "ratio": 7.53, "note": ""},
        {"name": "唐杰", "type": "natural", "ratio": 6.02, "note": "清华计算机系教授"},
        {"name": "珠海横琴智登企业管理合伙企业（有限合伙）", "type": "legal", "ratio": 5.18, "note": ""},
        {"name": "苏州君联相道股权投资合伙企业（有限合伙）", "type": "legal", "ratio": 4.19, "note": "君联资本"},
        {"name": "天津三快科技有限公司", "type": "legal", "ratio": 3.86, "note": "美团系"},
        {"name": "蚂蚁科技集团股份有限公司", "type": "legal", "ratio": 3.61, "note": "蚂蚁集团"},
        {"name": "华控技术转移有限公司", "type": "legal", "ratio": 3.48, "note": "清华控股"},
        {"name": "全德美嘉有限公司", "type": "legal", "ratio": 2.55, "note": ""},
        {"name": "陈浩", "type": "natural", "ratio": 1.89, "note": "智谱高管"},
        {"name": "李涓子", "type": "natural", "ratio": 0.76, "note": "清华教授"},
        {"name": "刘德兵", "type": "natural", "ratio": 0.21, "note": "董事长"},
        {"name": "许斌", "type": "natural", "ratio": 0.18, "note": ""},
        {"name": "张鹏", "type": "natural", "ratio": 0.09, "note": "CEO"},
    ],
    "月之暗面": [
        {"name": "杨植麟", "type": "natural", "ratio": 51.83, "note": "创始人/CEO/董事"},
        {"name": "深圳和谐成长三期科技发展股权投资基金合伙企业（有限合伙）", "type": "legal", "ratio": 11.76, "note": "红杉中国"},
        {"name": "周昕宇", "type": "natural", "ratio": 6.56, "note": "联合创始人"},
        {"name": "南昌和谐安瑞股权投资合伙企业（有限合伙）", "type": "legal", "ratio": 4.69, "note": "红杉系"},
        {"name": "华月创智（青岛）创业投资基金合伙企业（有限合伙）", "type": "legal", "ratio": 4.23, "note": ""},
        {"name": "社保基金长三角科技创新股权投资基金（上海）合伙企业（有限合伙）", "type": "legal", "ratio": 4.00, "note": "社保基金"},
        {"name": "吴育昕", "type": "natural", "ratio": 3.91, "note": ""},
        {"name": "张宇韬", "type": "natural", "ratio": 3.33, "note": "监事"},
        {"name": "青岛仪象奔富创业投资基金合伙企业（有限合伙）", "type": "legal", "ratio": 2.49, "note": ""},
        {"name": "前沿同创（扬州）产业升级股权投资基金合伙企业（有限合伙）", "type": "legal", "ratio": 2.03, "note": ""},
        {"name": "和谐远达（宜兴）文化产业投资基金（有限合伙）", "type": "legal", "ratio": 1.88, "note": "红杉系"},
        {"name": "共青城君弘前沿创业投资合伙企业（有限合伙）", "type": "legal", "ratio": 1.83, "note": ""},
        {"name": "临港前沿阿特斯扬州新能源股权投资基金合伙企业（有限合伙）", "type": "legal", "ratio": 1.44, "note": ""},
    ],
    "百川智能": [
        {"name": "王小川", "type": "natural", "ratio": 76.428, "note": "创始人/CEO"},
        {"name": "百川众智（北京）管理咨询合伙企业（有限合伙）", "type": "legal", "ratio": 20.0, "note": "员工持股平台"},
        {"name": "许志翰", "type": "natural", "ratio": 1.0, "note": ""},
        {"name": "高燃", "type": "natural", "ratio": 1.0, "note": ""},
        {"name": "茹立云", "type": "natural", "ratio": 0.772, "note": "联合创始人/监事"},
        {"name": "蒋又新", "type": "natural", "ratio": 0.4, "note": ""},
        {"name": "王子文", "type": "natural", "ratio": 0.2, "note": ""},
        {"name": "焦可", "type": "natural", "ratio": 0.2, "note": ""},
    ],
    "MiniMax": [
        {"name": "香港稀宇极智有限公司", "type": "legal", "ratio": 100.0, "note": "VIE 境外母公司"},
    ],
    "零一万物": [
        {"name": "北京零一万物智能技术有限公司", "type": "legal", "ratio": 100.0, "note": "WFOE 母公司"},
    ],
}

# ===== 实控人 =====
controllers = {
    "智谱": None,  # 未发现（公司治理结构特殊）
    "月之暗面": [
        {"name": "杨植麟", "direct": 51.83, "total": 51.83, "voting": 51.83, "note": "创始人绝对控股"}
    ],
    "百川智能": [
        {"name": "王小川", "direct": 76.428, "total": 92.428, "voting": 96.428, "note": "创始人绝对控股（含员工持股平台）"}
    ],
    "MiniMax": [
        {"name": "闫俊杰", "direct": 0, "total": 100, "voting": 100, "note": "通过 VIE 母公司 100% 实控"}
    ],
    "零一万物": [
        {"name": "零一万物（香港）有限公司", "total": 100, "voting": 100, "note": "李开复创新工场系"},
    ],
}

# ===== 已拉到的高管 =====
people_raw = [
    # 智谱（12 人）
    ("刘德兵", "智谱", "董事长,执行董事", 0.21, "2025-03-26 至今"),
    ("张鹏", "智谱", "执行董事,首席执行官,总经理", 0.09, "2024-01-01 至今"),
    ("张笑涵", "智谱", "执行董事", None, "2025-03-26 至今"),
    ("王盟", "智谱", "非执行董事", None, "2025-03-26 至今"),
    ("李涓子", "智谱", "非执行董事", 0.76, "2025-06-28 至今"),
    ("李家庆", "智谱", "非执行董事", None, "2025-03-26 至今"),
    ("谢德仁", "智谱", "独立非执行董事", None, "2025-06-28 至今"),
    ("杨强", "智谱", "独立非执行董事", None, "2025-06-28 至今"),
    ("徐文鸣", "智谱", "独立非执行董事", None, "2026-06-22 至今"),
    ("王绍兰", "智谱", "副总经理", None, "2019-07-01 至今"),
    ("郑程杰", "智谱", "公司秘书", None, "2025-06-01 至今"),
    ("肖磊", "智谱", "董事会秘书", None, "2025-12-18 至今"),
    # 月之暗面（3 人）
    ("杨植麟", "月之暗面", "董事", 51.83, ""),
    ("周昕宇", "月之暗面", "经理", 6.56, ""),
    ("张宇韬", "月之暗面", "监事", 3.33, ""),
    # 百川（3 人）
    ("王小川", "百川智能", "执行董事,经理", 76.428, ""),
    ("茹立云", "百川智能", "监事", 0.772, ""),
    ("孙鹏鹏", "百川智能", "财务负责人", None, ""),
    # MiniMax（3 人）
    ("闫俊杰", "MiniMax", "执行董事,经理", None, ""),
    ("任思源", "MiniMax", "监事", None, ""),
    ("缑月", "MiniMax", "财务负责人", None, ""),
    # 零一万物（3 人）
    ("马杰", "零一万物", "执行董事,经理", None, ""),
    ("叶静子", "零一万物", "监事", None, ""),
    ("曹桢", "零一万物", "财务负责人", None, ""),
]

# ===== 写文件 =====
data = {
    "summary": {
        "total_companies": len(companies),
        "data_source": "企查查 API (2026-07-13/14)",
        "data_quality": {
            "registration_info": "12/12 ✅",
            "shareholders": "5/12 ✅ (智谱/月之暗面/百川/MiniMax/零一万物)",
            "controller": "4/12 ✅",
            "key_personnel": "5/12 ✅",
        },
        "remaining_to_scrape": ["阶跃星辰", "生数科技", "深度求索", "面壁智能", "衔远科技", "无问芯穹", "瑞莱智慧"],
    },
    "companies": companies,
    "shareholders_by_company": shareholders,
    "controllers_by_company": controllers,
    "people_raw": [
        {"name": n, "company": c, "position": p, "shareholding": s, "term": t}
        for n, c, p, s, t in people_raw
    ],
}

with open(OUT / "llm_data_v3_partial.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ 已落盘 → {OUT / 'llm_data_v3_partial.json'}")
print(f"   公司: {len(companies)}")
print(f"   股东数据: {len(shareholders)} 家公司")
print(f"   实控人: {sum(1 for c in controllers.values() if c)} 家公司")
print(f"   高管: {len(people_raw)} 人")
print()
print("⚠️ 缺数据的 7 家公司: 阶跃星辰 / 生数科技 / 深度求索 / 面壁智能 / 衔远科技 / 无问芯穹 / 瑞莱智慧")
print("   建议: 用 web_search 补股东信息（蚂蚁/腾讯/阿里/字节等大厂投资关系都是公开新闻）")

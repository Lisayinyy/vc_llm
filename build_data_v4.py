"""LLM v4 数据 — 投资方中心 + 老大穿透 + 公司关系"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
src = json.load(open(BASE / 'llm_data_v3_full.json'))

# 6 个老大 (来自 web 公开人物调研)
bosses = [
    {"id":"b_alibaba","name":"阿里系 (蔡崇信+吴泳铭)","title_short":"阿里战投",
     "company":"阿里巴巴","covers":["智谱","百川智能","MiniMax","月之暗面","零一万物"],
     "note":"12 强里投了 5 家的最大金主, 阿里云算力支付","src":"🟠 公开新闻"},
    {"id":"b_qiming","name":"邝子平","title_short":"启明创投",
     "company":"启明创投","covers":["无问芯穹","生数科技","衔远科技","阶跃星辰"],
     "note":"跨 4 家 12 强, 中国 AI VC 最深 GP","src":"🟠 公开新闻"},
    {"id":"b_bjfund","name":"北京 AI 产业基金 (启明+京国管 GP)","title_short":"北京 AI 国资",
     "company":"北京市人工智能产业投资基金","covers":["瑞莱智慧","生数科技","面壁智能"],
     "note":"100 亿母基金, 启欧管理 (启明) + 京国管 (北京国资) 双 GP","src":"🟢 qichacha"},
    {"id":"b_shennp","name":"沈南鹏","title_short":"红杉中国",
     "company":"红杉中国","covers":["阶跃星辰","无问芯穹"],
     "note":"红杉中国 创始及执行合伙人, 中国 VC 教父","src":"🟠 公开新闻"},
    {"id":"b_xiong","name":"熊晓鸽","title_short":"IDG 资本",
     "company":"IDG 资本","covers":["阶跃星辰","深度求索"],
     "note":"IDG 创始合伙人, DeepSeek 早期最重要资本方","src":"🟠 公开新闻"},
    {"id":"b_jigang","name":"纪纲","title_short":"蚂蚁战投",
     "company":"蚂蚁集团","covers":["瑞莱智慧","生数科技"],
     "note":"蚂蚁集团 副总裁 / 战投总裁, 大模型+具身最积极大厂 CVC","src":"🟠 公开新闻"},
]

# boss ↔ investor 关系
boss_inv = [
    ("启明创投","b_qiming"),("启欧管理","b_qiming"),
    ("红杉中国","b_shennp"),("红杉种子","b_shennp"),
    ("IDG资本","b_xiong"),
    ("蚂蚁集团","b_jigang"),("上海云鑫","b_jigang"),
    ("阿里巴巴","b_alibaba"),("阿里云","b_alibaba"),
    ("北京市人工智能产业投资基金","b_bjfund"),
    ("京国管","b_bjfund"),("北京市政府投资引导基金","b_bjfund"),
]

# 公司 ↔ 公司 关系 (通过共同投资方)
# 走 multi_company_investors 算出哪两家公司被同一投资方投了
mci = src['multi_company_investors']
edges_comp_comp = []
for inv, comps in mci.items():
    if len(comps) >= 2:
        for i, a in enumerate(comps):
            for b in comps[i+1:]:
                edges_comp_comp.append({
                    "from": a, "to": b, "via": inv,
                    "type": "co_invested"
                })

# 老大排行
boss_rank = sorted([{"name":b['name'],"title":b['title_short'],
                     "count":len(b['covers']),"covers":b['covers']} for b in bosses],
                   key=lambda x: -x['count'])

# 默认中心
default_center = "启明创投"

out = {
    "version": "v4",
    "summary": src['summary'],
    "default_center": default_center,
    "default_center_reason": "跨公司投资方中投了 4 家 12 强最多",
    "companies": src['companies'],
    "shareholders_by_company": src['shareholders_by_company'],
    "controllers_by_company": src['controllers_by_company'],
    "multi_company_investors": mci,
    "company_company_edges": edges_comp_comp,  # 新增: 公司 ↔ 公司 通过共同投资方
    "bosses": bosses,
    "boss_investor_relations": [{"investor":a,"boss_id":b} for a,b in boss_inv],
    "boss_coverage_ranked": boss_rank,
    "data_discipline": src.get('data_discipline', {}),
}

(BASE / 'llm_data_v4.json').write_text(json.dumps(out, ensure_ascii=False, indent=2))
print(f"✅ v4 data: {len(bosses)} bosses | {len(edges_comp_comp)} company↔company edges")
print(f"   default center = {default_center}")
print()
print("=== 跨公司老大排行 ===")
for i,b in enumerate(boss_rank, 1):
    print(f"  {i}. {b['name']} → 投了 {b['count']} 家: {b['covers']}")
print()
print(f"=== 公司↔公司关系 (前 10) ===")
for e in edges_comp_comp[:10]:
    print(f"  {e['from']} ↔ {e['to']} (via {e['via']})")
print(f"  ... 共 {len(edges_comp_comp)} 条")

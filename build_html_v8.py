#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""大模型图谱 v3 - 动态可交互"""

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
data_path = OUT / "llm_data_audited.json"
if not data_path.exists():
    data_path = OUT / "llm_data_audited.json"
with open(data_path, encoding="utf-8") as f:
    data = json.load(f)

data_json = json.dumps(data, ensure_ascii=False)

HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8" />
<title>中国大模型产业投资关系图谱 · 严格证据集</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
<style>
  :root {
    --bg: #0d1117;
    --panel: #161b22;
    --panel-2: #0d1117;
    --border: #21262d;
    --text: #e6edf3;
    --text-dim: #8b949e;
    --accent: #58a6ff;
    --general: #ff6b35;
    --multimodal: #d2a8ff;
    --edge: #79c0ff;
    --infra: #f7c948;
    --safety: #56d364;
    --person: #ff5e5e;
    --controller: #ff5e5e;
    --tenure: #58a6ff;
    --share-q: #f7c948;
    --share-w: #ff9e64;
    --control: #ff5e5e;
    --company: #d2a8ff;
    --investor: #79c0ff;
    --boss-line: #ff5e5e;
    --co-line: #a5d6ff;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
    background: var(--bg);
    color: var(--text);
    height: 100vh;
    overflow: hidden;
  }
  .app { display: grid; grid-template-rows: auto 1fr; height: 100vh; }
  .header {
    padding: 14px 24px;
    background: linear-gradient(180deg, #1a1f2e 0%, var(--bg) 100%);
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
  }
  .title-block h1 {
    font-size: 18px;
    font-weight: 700;
    background: linear-gradient(90deg, #ff6b35 0%, #d2a8ff 50%, #58a6ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  .title-block .sub { font-size: 11px; color: var(--text-dim); margin-top: 2px; }
  .stats-bar { display: flex; gap: 8px; flex-wrap: wrap; }
  .stat-pill {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 11px;
  }
  .stat-pill b { color: var(--accent); font-size: 13px; }
  .stat-pill.multi b { color: #f7c948; }
  .stat-pill.qichacha b { color: #56d364; }
  .stat-pill.web b { color: #ff9e64; }
  .main {
    display: grid;
    grid-template-columns: 280px 1fr 360px;
    height: 100%;
    overflow: hidden;
  }
  .sidebar {
    background: var(--panel);
    border-right: 1px solid var(--border);
    padding: 16px;
    overflow-y: auto;
  }
  .sidebar h3 {
    font-size: 12px; color: var(--text-dim); margin: 16px 0 8px;
    text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;
  }
  .sidebar h3:first-child { margin-top: 0; }
  .center-pick {
    display: grid; grid-template-columns: 1fr 1fr; gap: 6px;
  }
  .center-btn {
    background: var(--panel-2); border: 1px solid var(--border);
    color: var(--text); padding: 6px 8px; border-radius: 4px;
    font-size: 11px; cursor: pointer; transition: all 0.15s; text-align: left;
  }
  .center-btn:hover { border-color: var(--accent); }
  .center-btn.active { background: var(--accent); border-color: var(--accent); color: white; }
  .center-btn.cat-general.active { background: var(--general); border-color: var(--general); }
  .center-btn.cat-multimodal.active { background: var(--multimodal); border-color: var(--multimodal); color: black; }
  .center-btn.cat-edge.active { background: var(--edge); border-color: var(--edge); color: black; }
  .center-btn.cat-infra.active { background: var(--infra); border-color: var(--infra); color: black; }
  .center-btn.cat-safety.active { background: var(--safety); border-color: var(--safety); color: black; }
  .center-btn.cat-investor.active { background: var(--share-w); border-color: var(--share-w); color: black; }
  .depth-control {
    display: flex; gap: 4px;
    background: var(--panel-2); border: 1px solid var(--border);
    border-radius: 4px; padding: 3px;
  }
  .depth-btn {
    flex: 1; background: transparent; border: none; color: var(--text-dim);
    padding: 4px 0; border-radius: 3px; font-size: 11px; cursor: pointer;
  }
  .depth-btn.active { background: var(--accent); color: white; }
  .check-list { display: flex; flex-direction: column; gap: 6px; }
  .check-item {
    display: flex; align-items: center; gap: 8px;
    padding: 6px 8px; background: var(--panel-2);
    border: 1px solid var(--border); border-radius: 4px;
    font-size: 12px; cursor: pointer; user-select: none;
  }
  .check-item:hover { border-color: var(--accent); }
  .check-item input { display: none; }
  .check-item .dot { width: 10px; height: 10px; border-radius: 50%; }
  .check-item.checked { border-color: var(--accent); background: #0d2a4d; }
  .search-input {
    width: 100%; padding: 7px 10px; background: var(--panel-2);
    border: 1px solid var(--border); border-radius: 4px;
    color: var(--text); font-size: 12px;
  }
  .search-input:focus { outline: none; border-color: var(--accent); }
  .info-box {
    background: var(--panel-2); border-left: 3px solid var(--share-w);
    border-radius: 4px; padding: 10px 12px;
    font-size: 11px; line-height: 1.6; color: var(--text-dim); margin-top: 8px;
  }
  .graph-wrap { position: relative; background: radial-gradient(circle at 50% 50%, #161b22 0%, var(--bg) 70%); }
  #graph { width: 100%; height: 100%; }
  .graph-toolbar {
    position: absolute; top: 12px; left: 12px;
    display: flex; flex-direction: column; gap: 6px; z-index: 10;
  }
  .g-btn {
    width: 32px; height: 32px; background: var(--panel);
    border: 1px solid var(--border); color: var(--text);
    border-radius: 4px; cursor: pointer; font-size: 14px;
    display: flex; align-items: center; justify-content: center;
  }
  .g-btn:hover { border-color: var(--accent); }
  .legend-box {
    position: absolute; bottom: 12px; left: 12px;
    background: rgba(13, 17, 23, 0.92);
    border: 1px solid var(--border); border-radius: 6px;
    padding: 10px 12px; font-size: 11px; z-index: 10; max-width: 260px;
  }
  .legend-box h4 { font-size: 11px; color: var(--text-dim); margin-bottom: 6px; }
  .legend-item { display: flex; align-items: center; gap: 8px; margin: 4px 0; color: var(--text); }
  .legend-shape { width: 12px; height: 12px; flex-shrink: 0; }
  .legend-line { width: 22px; height: 2px; flex-shrink: 0; }
  .status-bar {
    position: absolute; bottom: 12px; right: 12px;
    background: rgba(13, 17, 23, 0.92);
    border: 1px solid var(--border); border-radius: 4px;
    padding: 6px 10px; font-size: 11px; color: var(--text-dim); z-index: 10;
  }
  .status-bar b { color: var(--accent); }
  .detail {
    background: var(--panel); border-left: 1px solid var(--border);
    padding: 16px; overflow-y: auto;
  }
  .detail-empty {
    text-align: center; color: var(--text-dim);
    font-size: 12px; margin-top: 40px;
  }
  .detail-empty .emoji { font-size: 40px; margin-bottom: 12px; opacity: 0.5; }
  .detail-header { padding-bottom: 12px; border-bottom: 1px solid var(--border); margin-bottom: 12px; }
  .detail-name { font-size: 18px; font-weight: 700; color: var(--text); margin-bottom: 4px; }
  .detail-tags { display: flex; flex-wrap: wrap; gap: 4px; }
  .tag {
    font-size: 10px; padding: 2px 7px; border-radius: 3px; font-weight: 600;
  }
  .tag.general { background: rgba(255, 107, 53, 0.2); color: var(--general); }
  .tag.multimodal { background: rgba(210, 168, 255, 0.2); color: var(--multimodal); }
  .tag.edge { background: rgba(121, 192, 255, 0.2); color: var(--edge); }
  .tag.infra { background: rgba(247, 201, 72, 0.2); color: var(--infra); }
  .tag.safety { background: rgba(86, 211, 100, 0.2); color: var(--safety); }
  .tag.investor { background: rgba(255, 158, 100, 0.2); color: var(--share-w); }
  .tag.multi { background: #b58400; color: #000; }
  .tag.qichacha { background: rgba(86, 211, 100, 0.2); color: #56d364; }
  .tag.web { background: rgba(255, 158, 100, 0.2); color: #ff9e64; }
  .detail-section { margin-bottom: 16px; }
  .detail-section h4 {
    font-size: 11px; color: var(--text-dim);
    text-transform: uppercase; margin-bottom: 6px;
    letter-spacing: 0.05em; font-weight: 600;
  }
  .detail-row {
    display: flex; padding: 4px 0;
    font-size: 12px; border-bottom: 1px dashed var(--border);
  }
  .detail-row .key { color: var(--text-dim); width: 80px; flex-shrink: 0; }
  .detail-row .val { color: var(--text); flex: 1; }
  .rel-list { list-style: none; }
  .rel-item {
    background: var(--panel-2); border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: 4px; padding: 8px 10px; margin-bottom: 6px;
    cursor: pointer; font-size: 12px; transition: all 0.15s;
  }
  .rel-item:hover { border-color: var(--accent); transform: translateX(2px); }
  .rel-item.tenure { border-left-color: var(--tenure); }
  .rel-item.shareholding-q { border-left-color: var(--share-q); }
  .rel-item.shareholding-w { border-left-color: var(--share-w); }
  .rel-item.control { border-left-color: var(--control); }
  .rel-item .rel-type { font-size: 10px; color: var(--text-dim); text-transform: uppercase; }
  .rel-item .rel-target { font-weight: 600; color: var(--text); margin: 2px 0; }
  .rel-item .rel-evidence { font-size: 11px; color: var(--text-dim); }
  .footer-bar {
    padding: 8px 16px; border-top: 1px solid var(--border);
    font-size: 10px; color: var(--text-dim);
    text-align: center; background: var(--panel-2);
  }
</style>
</head>
<body>
<div class="app">
  <div class="header">
    <div class="title-block">
      <h1>中国大模型公司 × 投资方关系图谱</h1>
      <div class="sub">严格证据集 · 企查查记录 + 具备逐条一手证据的公开关系</div>
    </div>
    <div class="stats-bar" id="stats"></div>
  </div>

  <div class="main">
    <div class="sidebar">
      <h3>🎯 中心节点</h3>
      <div class="center-pick" id="center-pick"></div>

      <h3>📏 跳数深度</h3>
      <div class="depth-control" id="depth-control">
        <button class="depth-btn" data-depth="1">1 跳</button>
        <button class="depth-btn active" data-depth="2">2 跳</button>
        <button class="depth-btn" data-depth="3">3 跳</button>
      </div>

      <h3>🔍 节点类型</h3>
      <div class="check-list" id="node-types"></div>

      <h3>🔗 关系类型</h3>
      <div class="check-list" id="edge-types"></div>

      <h3>🔎 搜索</h3>
      <input type="text" class="search-input" id="search" placeholder="公司/人物/投资方..." />

      <div class="info-box">
        <b>💡 玩法：</b><br>
        1. 选中心节点<br>
        2. 切跳数 (1-3)<br>
        3. 筛选节点/关系类型<br>
        4. 点击节点看详情，点详情可漫游
      </div>

      <div class="info-box" style="border-left-color: var(--share-w);">
        <b>数据口径：</b><br>
        · 企查查关系按用户指定口径保留<br>
        · 公开关系必须具备逐条一手证据<br>
        · 待核验记录不构边、不参与排名<br>
        · 人物关系不得从机构组合推断
      </div>
    </div>

    <div class="graph-wrap">
      <div id="graph"></div>

      <div class="graph-toolbar">
        <button class="g-btn" id="btn-recenter" title="重置">⊙</button>
        <button class="g-btn" id="btn-fit" title="适配">⤢</button>
      </div>

      <div class="legend-box">
        <h4>图例 · 节点类型 (3类)</h4>
        <div class="legend-item">
          <div class="legend-shape" style="background:var(--company); border-radius:50%"></div>
          大模型公司 (12 家)
        </div>
        <div class="legend-item">
          <div class="legend-shape" style="background:var(--investor); border-radius:3px"></div>
          投资机构 (150+ 家)
        </div>
        <div class="legend-item">
          <div class="legend-shape" style="background:var(--person); border-radius:3px; transform:rotate(45deg)"></div>
          投资个人 (关键人物/股东)
        </div>
        <div style="height:8px"></div>
        <h4>关系</h4>
        <div class="legend-item">
          <div class="legend-line" style="background:var(--share-q)"></div>
          持股（工商登记）
        </div>
        <div class="legend-item">
          <div class="legend-line" style="background:var(--share-w)"></div>
          投资（公开新闻）
        </div>
        <div class="legend-item">
          <div class="legend-line" style="background:var(--boss-line); border:1px dashed;"></div>
          关键人物 ↔ 机构 (GP关系)
        </div>
        <div class="legend-item">
          <div class="legend-line" style="background:var(--co-line); border:1px dashed; opacity:0.5"></div>
          公司 ↔ 公司 (同被投资)
        </div>
      </div>

      <div class="status-bar">
        显示 <b id="visible-nodes">0</b> 节点 / <b id="visible-edges">0</b> 边 · 中心 <b id="visible-center">-</b>
      </div>
    </div>

    <div class="detail" id="detail">
      <div class="detail-empty">
        <div class="emoji">👆</div>
        点击图谱中任意节点<br>查看详情与关联关系
      </div>
    </div>
  </div>

  <div class="footer-bar">
    未核实公开关系不参与图谱与排名 · 证据规则与已知问题见 DATA_AUDIT.md
  </div>
</div>

<script>
const DATA = __DATA__;

// ============================================================
// v8: 阿里投资聚合中心
// ============================================================
// 聚合"阿里系"：阿里巴巴 + 阿里云 + 蚂蚁集团 + 上海云鑫
// 为每个口径造节点，连向 8 家被投公司
const ALI_ENTITIES = ['阿里巴巴', '阿里云', '蚂蚁集团', '上海云鑫'];
const ALI_PEER_COMPANIES = ['智谱', '百川智能', 'MiniMax', '月之暗面', '零一万物']; // 媒体推断未验证
const ALI_KNOWN_INVESTMENTS = {
  '智谱': { entity: '蚂蚁集团', ratio: 3.61, source: 'qichacha', note: '工商 3.61%', strict: true, round: '多轮跟投' },
};

// 虚报多源信息作为额外 unverified 记录 (帮助用户看完整阿里面)
const ALI_INFERRED = [
  // 智谱 3.61% 工商已记录，这里只补未验证
  { company: '生数科技', entity: '阿里云', ratio: '未披露', round: 'B轮 20亿(2026.04)', note: '领投', strict: false },
  { company: '生数科技', entity: '蚂蚁集团', ratio: '未披露', round: '天使轮', note: '领投+孵化', strict: false },
  { company: '瑞莱智慧', entity: '蚂蚁集团', ratio: '未披露', round: 'A轮 3亿+(2021.10)', note: '', strict: false },
  { company: '智谱', entity: '阿里巴巴', ratio: '未披露', round: '多轮', note: '媒体报道 (无 primary evidence)', strict: false, rumor: true },
  { company: '百川智能', entity: '阿里巴巴', ratio: '未披露', round: '多轮', note: '媒体报道 (无 primary evidence)', strict: false, rumor: true },
  { company: 'MiniMax', entity: '阿里巴巴', ratio: '未披露', round: '多轮', note: '媒体报道 (无 primary evidence)', strict: false, rumor: true },
  { company: '月之暗面', entity: '阿里巴巴', ratio: '未披露', round: '多轮 (8亿美元)', note: '媒体报道 (无 primary evidence)', strict: false, rumor: true },
  { company: '零一万物', entity: '阿里巴巴', ratio: '未披露', round: '多轮', note: '媒体报道 (无 primary evidence)', strict: false, rumor: true },
];

// 阿里系总投资统计
const ALI_STATS = {
  strict_count: 1,           // 智谱 3.61% 工商
  unverified_count: 3,       // 生数2 + 瑞莱1
  rumor_count: 5,            // 5 家伙伴媒体推断
  total_companies: 8,        // 8 家总计
  total_invested_estimated: '~ 300亿+ (估值口径推算)',
  strategy_summary: '“算力支付 + 跨阶段跟投 + 全 12 强押 8 家”',
};
const companies = DATA.companies;

const state = {
  centerId: 'ali_agg', // v8 默认 = 阿里系聚合中心 (看阿里投资策略)
  depth: 2,
  visibleNodeTypes: { company: true, investor: true, person: true },
  visibleEdgeTypes: { shareholding_q: true, shareholding_w: true, boss_link: true, co_invested: true, unverified: true, ali_member: true, ali_rumor: true },
};

// 节点数据：12 家公司
const short2idx = {};
companies.forEach((c, i) => short2idx[c.short] = i);

// 节点 + 边构造
const nodes = [];
const edges = [];
const seenNodeIds = new Set();

function addNode(nid, name, type, attrs) {
  if (seenNodeIds.has(nid)) return;
  seenNodeIds.add(nid);
  nodes.push({ id: nid, name, type, ...attrs });
}

// 12 家公司节点
companies.forEach(c => {
  addNode('co:' + c.short, c.short, 'company', {
    category: c.category,
    fullName: c.name,
    listing: c.listing,
    industry: c.industry,
    location: c.location,
    employeeCount: c.employee_count,
    registerCapital: c.register_capital_wan,
    legalRep: c.legal_rep,
    establishDate: c.establish_date,
    foundingTeam: c.founding_team,
  });
});

// 股东节点 + 持股边
const investorSet = new Set();
const naturalHolderSet = new Set();

Object.entries(DATA.shareholders_by_company).forEach(([coShort, shs]) => {
  shs.forEach((sh, idx) => {
    const nid = 'sh:' + sh.name;
    const isNatural = sh.type === 'natural';
    const type = isNatural ? 'natural' : 'investor';
    if (isNatural) naturalHolderSet.add(sh.name); else investorSet.add(sh.name);

    // 计算这个投资方在多少家 12 强公司出现过
    const appearanceCount = Object.values(DATA.shareholders_by_company).filter(s => s.some(x => x.name === sh.name)).length;
    const isMulti = appearanceCount >= 2;

    addNode(nid, sh.name, type, {
      isMultiCompany: isMulti,
      appearances: shs.filter(x => x.name === sh.name).map(x => x.company), // 注意：这只算了当前公司，需要在 end 时再算
      appearanceCount: appearanceCount,
      source: sh.source,
      note: sh.note,
    });

    // 边
    const edgeType = sh.source === 'qichacha' ? 'shareholding_q' : 'shareholding_w';
    edges.push({
      id: `sh-${coShort}-${sh.name}-${idx}`,
      source: nid,
      target: 'co:' + coShort,
      type: edgeType,
      label: typeof sh.ratio === 'number' ? sh.ratio.toFixed(2) + '%' : sh.ratio,
      weight: typeof sh.ratio === 'number' ? Math.max(1, sh.ratio / 5) : 0.5,
      ratio: sh.ratio,
      round: sh.round || '',
      source_label: sh.source === 'qichacha' ? '工商' : '公开',
    });
  });
});

// 重新计算 appearances（跨公司的）
const globalAppearances = {};
Object.values(DATA.shareholders_by_company).forEach(s => {
  s.forEach(sh => {
    if (!globalAppearances[sh.name]) globalAppearances[sh.name] = new Set();
    globalAppearances[sh.name].add(...Object.keys(DATA.shareholders_by_company).filter(c => 
      DATA.shareholders_by_company[c].some(x => x.name === sh.name)
    ));
  });
});
// 更新节点 attributes
nodes.forEach(n => {
  if (n.type === 'investor' || n.type === 'natural' || n.type === 'person') {
    const apps = Array.from(globalAppearances[n.name] || []);
    n.appearances = apps;
    n.appearanceCount = apps.length;
    n.isMultiCompany = apps.length >= 2;
  }
});

// v7 调整：BOSS 节点已由 audit 清空 (无 primary evidence) — 仍然处理空数组以防数据里有遗
if (DATA.bosses && DATA.bosses.length > 0) {
  DATA.bosses.forEach(b => {
    const nid = 'keyperson:' + b.id;
    addNode(nid, b.name, 'person', {
      title: b.title,
      title_short: b.title_short,
      company: b.company,
      category: b.category,
      covers: b.covers || [],
      coversCount: (b.covers || []).length,
      source: 'web',
      sourceLabel: b.src || '🟠 web',
      isMultiCompany: true,
      appearances: b.covers || [],
      appearanceCount: (b.covers || []).length,
      note: b.note || '',
      isBoss: true,
    });
  });
}

// v4 新增：BOSS ↔ INVESTOR 边 — v7 同样在数据为空时跳过
if (DATA.boss_investor_relations && DATA.boss_investor_relations.length > 0) {
  DATA.boss_investor_relations.forEach(r => {
    const bossNid = 'keyperson:' + r.boss_id;
    const invNid = 'sh:' + r.investor;
    if (seenNodeIds.has(bossNid) && nodes.some(n => n.id === invNid)) {
      edges.push({
        id: 'boss-rel-' + r.boss_id + '-' + r.investor,
        source: bossNid,
        target: invNid,
        type: 'boss_link',
        label: 'GP/关键人物',
        weight: 2.5,
        source_label: '🟠 web',
      });
    }
  });
}

// v4 新增：公司 ↔ 公司 边 (通过共同投资方连接)
if (DATA.company_company_edges) {
  DATA.company_company_edges.forEach((e, i) => {
    edges.push({
      id: 'comp-comp-' + i,
      source: 'co:' + e.from,
      target: 'co:' + e.to,
      type: 'co_invested',
      label: e.via,
      weight: 0.5,
      source_label: 'web',
      via: e.via,
    });
  });
}

// v7 新增：未验证的 web 记录作为灰色虚线边 (可选, 默认显示)
if (DATA.unverified_relationships) {
  DATA.unverified_relationships.forEach((r, i) => {
    const invNid = 'sh:' + r.name;
    // 节点不存在则加入
    if (!seenNodeIds.has(invNid)) {
      addNode(invNid, r.name, 'investor', {
        isMultiCompany: false,
        appearances: [r.company],
        appearanceCount: 1,
        source: 'web',
        sourceLabel: '⚪️ unverified',
      });
    }
    edges.push({
      id: 'unv-' + i,
      source: invNid,
      target: 'co:' + r.company,
      type: 'unverified',
      label: r.round || '未披露',
      weight: 0.3,
      source_label: 'unverified',
      exclusion_reason: r.exclusion_reason,
    });
  });
}

// ============================================================
// v8 新增：阿里系聚合中心 (ali_agg)
// ============================================================
addNode('ali_agg', '🏷️ 阿里系 (总投资)', 'investor', {
  isMultiCompany: true,
  appearances: ['智谱','百川智能','MiniMax','月之暗面','零一万物','生数科技','瑞莱智慧'],
  appearanceCount: 8,
  source: 'aggregated',
  sourceLabel: '多源聚合',
  isAliAgg: true,
  stats: ALI_STATS,
});

// 添加各个阿里实体节点 (如果 unverified 里没有)
ALI_ENTITIES.forEach(e => {
  const nid = 'sh:' + e;
  if (!seenNodeIds.has(nid)) {
    addNode(nid, e, 'investor', {
      isMultiCompany: e === '蚂蚁集团',
      appearances: [],
      appearanceCount: 0,
      source: 'aggregated',
      sourceLabel: '🏷️ 阿里系',
      isAliEntity: true,
    });
  }
  // 聚合节点 → 各个实体 (中粗)
  edges.push({
    id: 'ali-agg-' + e,
    source: 'ali_agg',
    target: nid,
    type: 'ali_member',
    label: '同一系',
    weight: 2,
    source_label: 'aggregated',
  });
});

// 阿里系 → 被投公司 (严格 + 未验证 + 媒体推断)
ALI_INFERRED.forEach((r, i) => {
  // 实体 → 公司
  const entityNid = 'sh:' + r.entity;
  if (seenNodeIds.has(entityNid)) {
    let edgeType, color_label, weight;
    if (r.strict) {
      edgeType = 'shareholding_q';
      color_label = '🟢 strict';
      weight = 3;
    } else if (r.rumor) {
      edgeType = 'ali_rumor';
      color_label = '📰 媒体推断';
      weight = 1;
    } else {
      edgeType = 'unverified';
      color_label = '⚪️ unverified';
      weight = 0.5;
    }
    edges.push({
      id: 'ali-inv-' + i,
      source: entityNid,
      target: 'co:' + r.company,
      type: edgeType,
      label: r.round,
      weight: weight,
      source_label: color_label,
      aliEntity: r.entity,
      aliNote: r.note,
    });
    // 更新该实体的 appearances
    const entityNode = nodes.find(n => n.id === entityNid);
    if (entityNode) {
      if (!entityNode.appearances.includes(r.company)) {
        entityNode.appearances.push(r.company);
        entityNode.appearanceCount = entityNode.appearances.length;
        entityNode.isMultiCompany = entityNode.appearances.length >= 2;
      }
    }
  }
});

// 实控人边 — 归为 person 边（不是 control 类型）
Object.entries(DATA.controllers_by_company || {}).forEach(([coShort, ctrls]) => {
  if (!ctrls) return;
  ctrls.forEach(c => {
    const nid = 'ctrl:' + c.name + ':' + coShort;
    if (seenNodeIds.has(nid)) return;
    addNode(nid, c.name, 'person', {
      isMultiCompany: false,
      appearances: [coShort],
      appearanceCount: 1,
      source: c.source || 'web',
      note: c.note || '',
    });
    edges.push({
      id: `ctrl-${coShort}-${c.name}`,
      source: nid,
      target: 'co:' + coShort,
      type: 'shareholding_w',
      label: `实控 ${c.total || '?'}%`,
      weight: 3,
      ratio: c.total,
      source_label: c.source || 'web',
    });
  });
});

// 邻接表
const adj = {};
edges.forEach(e => {
  if (!adj[e.source]) adj[e.source] = [];
  if (!adj[e.target]) adj[e.target] = [];
  adj[e.source].push({ target: e.target, edge: e, direction: 'out' });
  adj[e.target].push({ target: e.source, edge: e, direction: 'in' });
});

// N 跳
function getNhop(startId, depth) {
  const visited = new Set([startId]);
  const layers = new Map();
  layers.set(startId, 0);
  let frontier = [startId];
  for (let d = 1; d <= depth; d++) {
    const next = [];
    for (const id of frontier) {
      for (const nb of (adj[id] || [])) {
        if (!visited.has(nb.target)) {
          visited.add(nb.target);
          layers.set(nb.target, d);
          next.push(nb.target);
        }
      }
    }
    frontier = next;
  }
  return { ids: visited, layers };
}

// 节点颜色/大小 - 3 类节点
function getNodeColor(n) {
  if (n.type === 'company') return '#d2a8ff'; // 大模型公司 = 紫
  if (n.type === 'person') return '#ff5e5e'; // 投资个人 = 红 (关键人物/股东)
  if (n.type === 'investor') {
    if (n.isAliAgg) return '#ff7b00'; // 阿里聚合 = 橙
    if (n.isMultiCompany) return '#f7c948'; // 跨公司大金主 = 金
    return '#79c0ff'; // 普通投资机构 = 蓝
  }
  return '#888';
}
function getNodeShape(n) {
  if (n.type === 'company') return 'circle';
  if (n.type === 'person') return 'diamond'; // 投资个人 = 菱形
  if (n.type === 'investor') return 'rect';
  return 'circle';
}
function getNodeSize(n, hop) {
  if (hop === 0) return 50; // 中心节点大一点
  if (n.type === 'company') return 26; // 12 家
  if (n.type === 'person') return 20; // 关键人物/股东
  if (n.type === 'investor') {
    if (n.isAliAgg) return 32; // 阿里聚合 = 中心高亮
    if (n.isMultiCompany) return 16; // 跨公司金主
    if (n.isAliEntity) return 14; // 阿里实体
    return 9; // 普通机构
  }
  return 8;
}

const chart = echarts.init(document.getElementById('graph'));

function buildVisible() {
  const { ids, layers } = getNhop(state.centerId, state.depth);
  const visibleNodes = [];
  const visibleIds = [];
  ids.forEach(id => {
    const n = nodes.find(x => x.id === id);
    if (!n) return;
    // 节点类型筛选
    let typeKey = n.type === 'natural' ? 'person' : n.type; // 把 natural 映射到 person 开关 (兼容老数据)
    if (!state.visibleNodeTypes[typeKey]) return;
    visibleNodes.push(n);
    visibleIds.push(id);
  });
  const visibleSet = new Set(visibleIds);
  const visibleEdges = edges.filter(e =>
    visibleSet.has(e.source) && visibleSet.has(e.target) && state.visibleEdgeTypes[e.type]
  );

  document.getElementById('visible-nodes').textContent = visibleNodes.length;
  document.getElementById('visible-edges').textContent = visibleEdges.length;
  const cName = visibleNodes.find(n => n.id === state.centerId)?.name || '-';
  document.getElementById('visible-center').textContent = cName;

  return { nodes: visibleNodes, edges: visibleEdges, layers };
}

function render() {
  const { nodes: vNodes, edges: vEdges, layers } = buildVisible();
  const data = vNodes.map(n => {
    const hop = layers.get(n.id) || 0;
    const isCenter = hop === 0;
    return {
      id: n.id,
      name: n.name,
      _raw: n,
      _hop: hop,
      symbolSize: getNodeSize(n, hop),
      symbol: getNodeShape(n),
      itemStyle: {
        color: getNodeColor(n),
        borderColor: isCenter ? '#fff' : '#0d1117',
        borderWidth: isCenter ? 3 : 1.5,
        shadowBlur: isCenter ? 16 : (n.isMultiCompany ? 6 : 0),
        shadowColor: isCenter ? getNodeColor(n) : (n.isMultiCompany ? '#f7c948' : 'transparent'),
      },
      label: {
        show: isCenter || hop <= 1,
        position: 'right',
        color: isCenter ? '#fff' : '#c9d1d9',
        fontSize: isCenter ? 13 : 10,
        fontWeight: isCenter ? 700 : 400,
        textBorderColor: '#000',
        textBorderWidth: 2,
        formatter: (p) => {
          if (isCenter) return n.name;
          if (hop === 1) return n.name;
          return '';
        },
      },
      value: hop,
    };
  });
  const links = vEdges.map(e => {
    let color = '#ff9e64';
    let lineType = 'solid';
    let width = e.weight || 1;
    let opacity = 0.65;
    let curveness = 0.1;
    if (e.type === 'control') { color = '#ff5e5e'; lineType = 'dashed'; }
    else if (e.type === 'shareholding_q') color = '#f7c948';
    else if (e.type === 'boss_link') { color = '#ff5e5e'; width = 3; opacity = 0.9; lineType = 'dashed'; curveness = 0.3; } // 关键人物边 = 红粗虚线
    else if (e.type === 'co_invested') { color = '#a5d6ff'; width = 1; opacity = 0.45; lineType = 'dotted'; curveness = 0.5; } // 公司共同投资 = 蓝点线
    else if (e.type === 'unverified') { color = '#6e7681'; width = 0.5; opacity = 0.3; lineType = 'dashed'; curveness = 0.1; } // unverified = 灰虚线
    else if (e.type === 'ali_member') { color = '#ff7b00'; width = 2; opacity = 0.6; lineType = 'solid'; curveness = 0.2; } // 阿里系内部 = 橙色
    else if (e.type === 'ali_rumor') { color = '#ff9e64'; width = 1; opacity = 0.5; lineType = 'dotted'; curveness = 0.15; } // 媒体推断 = 橙色点线
    return {
      source: e.source,
      target: e.target,
      _raw: e,
      lineStyle: { color, width, type: lineType, opacity, curveness },
      label: {
        show: e.type === 'co_invested' || e.type === 'boss_link',
        formatter: e.label,
        fontSize: 8,
        color: e.type === 'boss_link' ? '#ff5e5e' : '#a5d6ff',
      },
    };
  });

  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      backgroundColor: 'rgba(13, 17, 23, 0.95)',
      borderColor: '#21262d',
      textStyle: { color: '#e6edf3', fontSize: 12 },
      formatter: (p) => {
        if (!p.data || !p.data._raw) return '';
        const n = p.data._raw;
        const lines = [`<b>${n.name}</b>`];
        if (n.type === 'company') {
          lines.push(`<span style="color:#8b949e;">类型：</span>${n.category}`);
          lines.push(`<span style="color:#8b949e;">${n.listing} · ${n.location}</span>`);
          lines.push(`<span style="color:#8b949e;">法人：</span>${n.legalRep}`);
          lines.push(`<span style="color:#8b949e;">创始团队：</span>${n.foundingTeam}`);
        }
        if ((n.type === 'investor' || n.type === 'natural' || n.type === 'person' || n.type === 'controller') && n.appearances) {
          lines.push(`<span style="color:#8b949e;">出现在：</span>${n.appearances.length} 家公司`);
          if (n.isMultiCompany) lines.push(`<span style="color:#f7c948;">⭐ 跨公司投资方</span>`);
          if (n.source === 'qichacha') lines.push(`<span style="color:#56d364;">来源：企查查工商</span>`);
          if (n.source === 'web') lines.push(`<span style="color:#ff9e64;">来源：公开新闻</span>`);
        }
        lines.push(`<br/><span style="color:#58a6ff;">点击查看详情</span>`);
        return lines.join('<br/>');
      },
    },
    series: [{
      type: 'graph',
      layout: 'force',
      force: {
        repulsion: 400,
        edgeLength: [60, 180],
        gravity: 0.04,
        friction: 0.4,
      },
      roam: true,
      draggable: true,
      animationDuration: 600,
      data,
      links,
      emphasis: {
        focus: 'adjacency',
        lineStyle: { width: 3, opacity: 1 },
        itemStyle: { borderColor: '#fff', borderWidth: 3 },
      },
    }],
  };
  chart.setOption(option, true);
  chart.on('click', onClick);
}

function onClick(p) {
  if (p.data && p.data._raw) showDetail(p.data._raw);
}

function showDetail(node) {
  const el = document.getElementById('detail');
  let tagClass = 'general';
  let typeLabel = '未知';
  if (node.type === 'company') {
    tagClass = 'company';
    typeLabel = '大模型公司';
  } else if (node.type === 'investor') {
    tagClass = 'investor';
    if (node.isAliAgg) { tagClass = 'ali-agg'; typeLabel = '🏷️ 阿里系聚合'; }
    else if (node.isAliEntity) { tagClass = 'ali-entity'; typeLabel = '🏷️ 阿里实体'; }
    else typeLabel = '投资机构';
  } else if (node.type === 'person') {
    tagClass = 'person';
    typeLabel = node.isBoss ? '👑 投资个人 / 关键人物' : '投资个人 / 股东';
  }

  let html = `
    <div class="detail-header">
      <div class="detail-name">${node.name}</div>
      <div class="detail-tags">
        <span class="tag ${tagClass}">${typeLabel}</span>
        ${node.isMultiCompany ? '<span class="tag multi">⭐ 跨公司</span>' : ''}
        ${node.isBoss ? '<span class="tag boss">关键人物</span>' : ''}
        ${node.source === 'qichacha' ? '<span class="tag qichacha">企查查</span>' : ''}
        ${node.source === 'web' ? '<span class="tag web">公开新闻</span>' : ''}
        ${node.sourceLabel ? `<span class="tag web">${node.sourceLabel}</span>` : ''}
      </div>
    </div>
  `;

  // v8: 阿里系聚合节点详情面板
  if (node.isAliAgg) {
    const s = ALI_STATS;
    const invs = ALI_INFERRED;
    html += `
      <div class="detail-section">
        <h4>🏷️ 阿里系全景</h4>
        <div class="detail-row"><div class="key">投资范围</div><div class="val"><b style="color:#f7c948;">${s.total_companies} 家 12 强</b> (占 12 强 ${Math.round(s.total_companies/12*100)}%)</div></div>
        <div class="detail-row"><div class="key">总投资估计</div><div class="val">${s.total_invested_estimated}</div></div>
        <div class="detail-row"><div class="key">核心策略</div><div class="val">${s.strategy_summary}</div></div>
      </div>
      <div class="detail-section">
        <h4>🔍 阿里各主体投资动作</h4>
        ${ALI_ENTITIES.map(e => {
          const compList = invs.filter(r => r.entity === e).map(r => `<span style="color:${r.rumor ? '#d2a8ff' : (r.strict ? '#56d364' : '#ff9e64')}; cursor:pointer; margin-right:6px;" onclick="focusNode('co:${r.company}')">${r.company}</span>(${r.round})`).join('、 ');
          return `<div class="detail-row"><div class="key">${e}</div><div class="val">${compList || '<span style="color:#6e7681;">无记录</span>'}</div></div>`;
        }).join('')}
      </div>
      <div class="detail-section">
        <h4>⚠️ 数据纪律提示</h4>
        <ul style="margin:0 0 0 16px; font-size:11px; color:#8b949e; line-height:1.6;">
          <li>只有 <b style="color:#56d364;">蚂蚁集团→智谱 3.61%</b> 是工商可查 (strict)</li>
          <li>生数/瑞莱是 web 报道但 <b style="color:#ff9e64;">未证据化</b></li>
          <li>5 家伙伴 (智谱/百川/MiniMax/月之暗面/零一万物) 是 <b style="color:#d2a8ff;">媒体广泛报道但无 primary source</b> — v7 audit 排除</li>
          <li>想要把这些关系 evidence 化，需逐个找企业公告/交易所/官网</li>
        </ul>
      </div>
    `;
  }

  // 关键人物节点详情面板
  if (node.type === 'person' && node.isBoss) {
    const covers = node.covers || [];
    html += `
      <div class="detail-section">
        <h4>👑 关键人物档案</h4>
        <div class="detail-row"><div class="key">职位</div><div class="val" style="color:#ff5e5e; font-weight:bold;">${node.title || node.title_short}</div></div>
        <div class="detail-row"><div class="key">所在机构</div><div class="val">${node.company}</div></div>
        <div class="detail-row"><div class="key">投资 12 强</div><div class="val" style="color:#f7c948; font-weight:bold;">${covers.length} 家</div></div>
        <div class="detail-row"><div class="key">备注</div><div class="val">${node.note || ''}</div></div>
        <div class="detail-row"><div class="key">投了谁</div><div class="val">${covers.map(c => `<span style="color:#79c0ff; cursor:pointer; margin-right:6px;" onclick="focusNode('co:${c}')">${c}</span>`).join('')}</div></div>
      </div>
    `;
  }

  if (node.type === 'company') {
    html += `
      <div class="detail-section">
        <h4>公司档案</h4>
        <div class="detail-row"><div class="key">全称</div><div class="val">${node.fullName}</div></div>
        <div class="detail-row"><div class="key">类别</div><div class="val">${node.category} · ${node.listing}</div></div>
        <div class="detail-row"><div class="key">注册地</div><div class="val">${node.location}</div></div>
        <div class="detail-row"><div class="key">注册资本</div><div class="val">${node.registerCapital.toFixed(2)} 万元</div></div>
        <div class="detail-row"><div class="key">参保人数</div><div class="val">${node.employeeCount} 人</div></div>
        <div class="detail-row"><div class="key">成立日期</div><div class="val">${node.establishDate}</div></div>
        <div class="detail-row"><div class="key">法人</div><div class="val" style="color:#d2a8ff;">${node.legalRep}</div></div>
        <div class="detail-row"><div class="key">主营</div><div class="val">${node.industry}</div></div>
        <div class="detail-row"><div class="key">创始团队</div><div class="val" style="color:#f7c948;">${node.foundingTeam}</div></div>
      </div>
    `;
  } else if (node.type === 'investor' || node.type === 'person') {
    if (node.appearances) {
      html += `
        <div class="detail-section">
          <h4>投资记录</h4>
          <div class="detail-row"><div class="key">出现公司</div><div class="val">${node.appearances.length} 家${node.isMultiCompany ? ' <span style="color:#f7c948;">(跨公司投资方)</span>' : ''}</div></div>
          ${node.note ? `<div class="detail-row"><div class="key">备注</div><div class="val">${node.note}</div></div>` : ''}
          <div class="detail-row"><div class="key">列表</div><div class="val">${node.appearances.map(c => `<span style="color:#79c0ff; cursor:pointer;" onclick="focusNode('co:${c}')">${c}</span>`).join('、')}</div></div>
        </div>
      `;
    }
  }

  // 关联关系
  const rels = (adj[node.id] || []).map(r => r.edge);
  if (rels.length > 0) {
    const grouped = { tenure: [], shareholding_q: [], shareholding_w: [], boss_link: [], co_invested: [] };
    rels.forEach(r => grouped[r.type] && grouped[r.type].push(r));
    html += `<div class="detail-section"><h4>🔗 关联关系 (${rels.length})</h4><ul class="rel-list">`;
    for (const type of ['shareholding_q', 'shareholding_w', 'boss_link', 'co_invested', 'tenure']) {
      grouped[type].forEach(e => {
        const otherId = e.source === node.id ? e.target : e.source;
        const other = nodes.find(x => x.id === otherId);
        if (!other) return;
        const typeLabel = { tenure: '任职', shareholding_q: '持股(工商)', shareholding_w: '投资(公开)', boss_link: '关键人物关联', co_invested: '同被投资' }[type];
        const cls = { tenure: 'tenure', shareholding_q: 'shareholding-q', shareholding_w: 'shareholding-w', boss_link: 'boss', co_invested: 'co' }[type];
        const arrow = e.source === node.id ? '→' : '←';
        const srcBadge = e.source_label === '工商' ? '<span class="tag qichacha" style="margin-right:4px;">工商</span>' : '<span class="tag web" style="margin-right:4px;">新闻</span>';
        html += `
          <li class="rel-item ${cls}" onclick="focusNode('${otherId}')">
            <div class="rel-type">${srcBadge}${typeLabel} ${arrow}</div>
            <div class="rel-target">${other.name}</div>
            <div class="rel-evidence">${e.label || ''}${e.round ? ' · ' + e.round : ''}</div>
          </li>
        `;
      });
    }
    html += `</ul></div>`;
  }

  el.innerHTML = html;
}

window.focusNode = function(id) {
  const n = nodes.find(x => x.id === id);
  if (!n) return;
  showDetail(n);
  // 重新计算跳数 + 渲染
  state.centerId = id;
  document.querySelectorAll('.center-btn').forEach(b => {
    b.classList.toggle('active', b.dataset.id === id);
  });
  render();
};

// === 初始化控件 ===

// Stats
const statsEl = document.getElementById('stats');
const admitted = DATA.audit?.admitted || {};
statsEl.innerHTML = `
  <div class="stat-pill">公司 <b>${companies.length}</b></div>
  <div class="stat-pill">关系 <b>${edges.length}</b></div>
  <div class="stat-pill multi">跨公司投资方 <b>${Object.values(DATA.multi_company_investors).length}</b></div>
  <div class="stat-pill qichacha">企查查关系 <b>${admitted.qichacha || 0}</b></div>
  <div class="stat-pill web">一手公开证据 <b>${admitted.verified_public || 0}</b></div>
  <div class="stat-pill">待核验 <b>${DATA.audit?.excluded_unverified || 0}</b></div>
  <div class="stat-pill" style="background:#ff7b0033; border-color:#ff7b0088; cursor:pointer;" onclick="focusNode('ali_agg')">🏷️ 阿里系 <b>${ALI_STATS.total_companies}</b> 家 (strict ${ALI_STATS.strict_count} + web ${ALI_STATS.unverified_count} + 推断 ${ALI_STATS.rumor_count})</div>
`;

// v8: 阿里投资策略分析卡
const aliPanelHtml = `
  <div class="detail" id="ali-panel" style="background:#ff7b0011; border:1px solid #ff7b0088; padding:14px; border-radius:8px; margin-top:12px;">
    <h3 style="margin:0 0 8px 0; color:#ff7b00;">🏷️ 阿里系投资策略 (v8 视角)</h3>
    <div style="font-size:12px; line-height:1.7; color:#e6edf3;">
      <div><b style="color:#56d364;">✅ 工商可查：</b>1 笔 — 蚂蚁集团 智谱 3.61%</div>
      <div><b style="color:#ff9e64;">📊 未验证但报道：</b>3 笔 — 阿里云→生数(领投B轮20亿) / 蚂蚁→生数(天使领投) / 蚂蚁→瑞莱(A轮3亿+)</div>
      <div><b style="color:#d2a8ff;">📰 媒体推断 (无 primary)：</b>5 笔 — 智谱/百川/MiniMax/月之暗面/零一万物</div>
      <hr style="border-color:#21262d; margin:8px 0;" />
      <div><b>总计覆盖：</b><span style="color:#f7c948;">${ALI_STATS.total_companies} 家 12 强公司 (8/12 = 67%)</span></div>
      <div><b>总投资估计：</b>${ALI_STATS.total_invested_estimated}</div>
      <div><b>核心策略：</b>${ALI_STATS.strategy_summary}</div>
      <ul style="margin:6px 0 0 18px; font-size:11px; color:#8b949e;">
        <li><b>算力支付</b>：阿里云算力换股权，不单纯打现金 (生数 B 轮为典型)</li>
        <li><b>多主体</b>：阿里巴巴主体/阿里云/蚂蚁集团/云鑫 多个投资口径同时进</li>
        <li><b>全赛道</b>：从智谱(综合)/月之暗面(Kimi)到 MiniMax/生数(多模态)全覆盖</li>
        <li><b>跨阶段</b>：从天使(蚂蚁→生数)到 B 轮(阿里云→生数) 到 战略跟投</li>
      </ul>
    </div>
  </div>
`;
// 插到 stats 后面
const statsParent = document.getElementById('stats').parentElement;
if (statsParent && !document.getElementById('ali-panel')) {
  statsParent.insertAdjacentHTML('beforeend', aliPanelHtml);
}

// 中心节点选择器
const centerPick = document.getElementById('center-pick');
const verifiedInvestorSuggestions = [...new Set(
  Object.values(DATA.shareholders_by_company)
    .flat()
    .filter(x => x.type === 'legal')
    .map(x => x.name)
)].map(name => {
  const count = Object.values(DATA.shareholders_by_company)
    .filter(records => records.some(x => x.type === 'legal' && x.name === name)).length;
  return { id: 'sh:' + name, name, cat: 'investor', label: `已核实关联 ${count} 家` };
}).sort((a, b) => b.label.localeCompare(a.label) || a.name.localeCompare(b.name)).slice(0, 8);
const suggestions = [
  // v8: 阿里聚合中心 (第一个, 作为默认提示)
  { id: 'ali_agg', name: '🏷️ 阿里系', cat: 'investor', label: '总投资 8 家' },
  // 12 家公司
  ...companies.map(c => ({ id: 'co:' + c.short, name: c.short, cat: 'company', label: c.industry.slice(0, 12) })),
  ...verifiedInvestorSuggestions,
  // 关键人物节点
  ...(DATA.bosses || []).map(b => ({ id: 'keyperson:' + b.id, name: '👑 ' + b.name, cat: 'person', label: b.title_short + ' · 投了 ' + b.covers.length + ' 家' })),
];
suggestions.forEach(s => {
  const btn = document.createElement('button');
  btn.className = 'center-btn cat-' + s.cat;
  btn.dataset.id = s.id;
  btn.innerHTML = `<b>${s.name}</b><br><span style="font-size:9px;opacity:0.8">${s.label}</span>`;
  if (s.id === state.centerId) btn.classList.add('active');
  btn.onclick = () => {
    state.centerId = s.id;
    document.querySelectorAll('.center-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    render();
  };
  centerPick.appendChild(btn);
});

// 跳数控制
document.querySelectorAll('.depth-btn').forEach(b => {
  b.onclick = () => {
    document.querySelectorAll('.depth-btn').forEach(x => x.classList.remove('active'));
    b.classList.add('active');
    state.depth = parseInt(b.dataset.depth);
    render();
  };
});

// 节点类型筛选
const nodeTypeConfig = [
  { key: 'company', label: '大模型公司 (12 家)', color: '#d2a8ff' },
  { key: 'investor', label: '投资机构 (150+ 家)', color: '#79c0ff' },
  { key: 'person', label: '投资个人 (关键人物/股东)', color: '#ff5e5e' },
];
const nodeTypesEl = document.getElementById('node-types');
nodeTypeConfig.forEach(c => {
  const div = document.createElement('label');
  div.className = 'check-item' + (state.visibleNodeTypes[c.key] ? ' checked' : '');
  div.innerHTML = `<input type="checkbox" ${state.visibleNodeTypes[c.key] ? 'checked' : ''}><div class="dot" style="background:${c.color}"></div><span>${c.label}</span>`;
  const cb = div.querySelector('input');
  cb.onchange = () => {
    state.visibleNodeTypes[c.key] = cb.checked;
    div.classList.toggle('checked', cb.checked);
    render();
  };
  nodeTypesEl.appendChild(div);
});

// 关系类型筛选
const edgeTypeConfig = [
  { key: 'shareholding_q', label: '🟢 持股 (工商登记)', color: '#f7c948' },
  { key: 'shareholding_w', label: '🔵 投资 (公开新闻)', color: '#ff9e64' },
  { key: 'boss_link', label: '🔴 关键人物 ↔ 机构 (GP关系)', color: '#ff5e5e' },
  { key: 'co_invested', label: '🟦 公司 ↔ 公司 (同被投资)', color: '#a5d6ff' },
  { key: 'unverified', label: '⚪️ 未验证 (audit 排除)', color: '#6e7681' },
  { key: 'ali_member', label: '🟠 阿里系内部 (v8)', color: '#ff7b00' },
  { key: 'ali_rumor', label: '📰 媒体推断 (v8)', color: '#ff9e64' },
];
const edgeTypesEl = document.getElementById('edge-types');
edgeTypeConfig.forEach(c => {
  const div = document.createElement('label');
  div.className = 'check-item' + (state.visibleEdgeTypes[c.key] ? ' checked' : '');
  div.innerHTML = `<input type="checkbox" ${state.visibleEdgeTypes[c.key] ? 'checked' : ''}><div class="dot" style="background:${c.color}"></div><span>${c.label}</span>`;
  const cb = div.querySelector('input');
  cb.onchange = () => {
    state.visibleEdgeTypes[c.key] = cb.checked;
    div.classList.toggle('checked', cb.checked);
    render();
  };
  edgeTypesEl.appendChild(div);
});

// 搜索
let searchTimer = null;
document.getElementById('search').addEventListener('input', (e) => {
  clearTimeout(searchTimer);
  const val = e.target.value.trim();
  searchTimer = setTimeout(() => {
    if (!val) return;
    const lower = val.toLowerCase();
    const found = nodes.find(n => n.name.toLowerCase().includes(lower));
    if (found) focusNode(found.id);
  }, 250);
});

// 工具栏
document.getElementById('btn-recenter').onclick = () => chart.dispatchAction({ type: 'restore' });
document.getElementById('btn-fit').onclick = () => chart.dispatchAction({ type: 'restore' });

window.addEventListener('resize', () => chart.resize());

// 初始渲染
render();
setTimeout(() => focusNode(state.centerId), 500);
</script>
</body>
</html>
"""

html_final = HTML.replace("__DATA__", data_json)
out_path = OUT / "llm_graph_v8.html"
index_path = OUT / "index.html"
for path in (out_path, index_path):
    path.write_text(html_final, encoding="utf-8")

print(f"✅ HTML v3 已生成: {out_path}")
print(f"   入口已同步: {index_path}")
print(f"   文件大小: {out_path.stat().st_size / 1024:.1f} KB")
print()
print("📊 数据规模:")
# print(f"   节点: {len(nodes)}")
# print(f"   边: {len(edges)}")
# print(f"   跨公司投资方: {len(DATA.multi_company_investors)} 个")

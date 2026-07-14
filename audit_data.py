#!/usr/bin/env python3
"""Build a strict, evidence-backed view of the investment graph."""

import json
from collections import Counter
from copy import deepcopy
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "llm_data_v4.json"
OUTPUT = ROOT / "llm_data_audited.json"
REPORT = ROOT / "DATA_AUDIT.md"

# Public-web relationships are admitted only after a human verifies the linked
# page and records what it proves. Search snippets are never evidence.
VERIFIED_PUBLIC = {
    ("无问芯穹", "启明创投", "A轮 近5亿"): {
        "relation": "invested_in",
        "status": "verified",
        "evidence_level": "primary",
        "publisher": "启明创投",
        "published_at": "2024-09-02",
        "accessed_at": "2026-07-14",
        "source_url": "https://www.qimingvc.com/cn/news/%E5%90%AF%E6%98%8E%E6%98%9F-%E6%97%A0%E9%97%AE%E8%8A%AF%E7%A9%B9%E8%8E%B7%E8%BF%9110%E4%BA%BF%E5%85%83%E7%B4%AF%E8%AE%A1%E8%9E%8D%E8%B5%84%EF%BC%8C%E5%90%AF%E6%98%8E%E5%88%9B%E6%8A%95%E8%81%94%E5%90%88%E9%A2%86%E6%8A%95a%E8%BD%AE",
        "evidence_quote": "无问芯穹获近10亿元累计融资，启明创投联合领投A轮",
    },
}

KNOWN_ISSUES = [
    {
        "severity": "critical",
        "scope": "all non-Qichacha relationships",
        "finding": "127 web records have no source URL, publication date, access date, or evidence quote.",
        "action": "Excluded from the strict graph until individually evidenced.",
    },
    {
        "severity": "critical",
        "scope": "person-to-company attribution",
        "finding": "The six boss coverage lists infer personal deal ownership from institutional portfolios.",
        "action": "Removed all boss coverage edges. Add a person only with a named deal lead, board seat, or equivalent primary evidence.",
    },
    {
        "severity": "high",
        "scope": "深度求索 A轮 510亿",
        "finding": "The dataset says 2026.05; the located report is dated 2026-06-18 and describes a June工商变更. No company or investor announcement was located.",
        "action": "Excluded pending primary evidence or a clearly labelled工商-derived record.",
    },
    {
        "severity": "high",
        "scope": "瑞莱智慧 strategic round",
        "finding": "The dataset says 2026.05, while the located report is dated 2024-04-12.",
        "action": "Excluded pending reconciliation with the original announcement.",
    },
    {
        "severity": "high",
        "scope": "relationship semantics",
        "finding": "Incubation, strategic cooperation, shareholders, and financing participants are stored in one shareholders list.",
        "action": "Only explicit shareholding or investment relationships are admitted to the strict graph.",
    },
    {
        "severity": "medium",
        "scope": "entity resolution",
        "finding": "Aliases such as 华勤/华勤技术 and 百度风投/BV百度风投/百度战投 are separate nodes.",
        "action": "Resolve to legal entities before restoring affected records.",
    },
]


def build_audited_data(raw):
    audited = deepcopy(raw)
    pending = []
    admitted = Counter()
    strict_shareholders = {}

    for company, records in raw["shareholders_by_company"].items():
        strict_shareholders[company] = []
        for record in records:
            item = deepcopy(record)
            if item.get("source") == "qichacha":
                item.update({
                    "status": "trusted_by_user",
                    "evidence_level": "registry",
                    "as_of": "2026-07-13/14",
                })
                strict_shareholders[company].append(item)
                admitted["qichacha"] += 1
                continue

            key = (company, item.get("name"), item.get("round"))
            evidence = VERIFIED_PUBLIC.get(key)
            if evidence:
                item.update(evidence)
                strict_shareholders[company].append(item)
                admitted["verified_public"] += 1
            else:
                item["status"] = "unverified"
                item["exclusion_reason"] = "missing_record_level_evidence"
                pending.append({"company": company, **item})

    portfolios = {}
    for company, records in strict_shareholders.items():
        for record in records:
            if record.get("type") != "legal":
                continue
            portfolios.setdefault(record["name"], set()).add(company)

    multi = {
        investor: sorted(companies)
        for investor, companies in portfolios.items()
        if len(companies) >= 2
    }

    strict_controllers = {}
    for company, records in raw["controllers_by_company"].items():
        if not records:
            strict_controllers[company] = records
            continue
        strict_controllers[company] = [
            {**deepcopy(record), "status": "trusted_by_user", "evidence_level": "registry"}
            for record in records
            if record.get("source") == "qichacha"
        ]

    audited.update({
        "version": "v4-audited-1",
        "audit": {
            "policy": "qichacha_trusted_by_user_plus_record_level_primary_evidence",
            "generated_at": str(date.today()),
            "admitted": dict(admitted),
            "excluded_unverified": len(pending),
            "known_issue_count": len(KNOWN_ISSUES),
        },
        "shareholders_by_company": strict_shareholders,
        "controllers_by_company": strict_controllers,
        "unverified_relationships": pending,
        "multi_company_investors": multi,
        "company_company_edges": [],
        "bosses": [],
        "boss_investor_relations": [],
        "boss_coverage_ranked": [],
        "default_center": "智谱",
        "default_center_reason": "严格证据集暂不支持原有跨公司投资方排名",
    })
    audited["summary"] = {
        **raw["summary"],
        "audit_status": "strict",
        "verified_relationships": sum(admitted.values()),
        "unverified_relationships": len(pending),
        "verified_public_relationships": admitted["verified_public"],
    }
    return audited, pending, admitted


def render_report(pending, admitted):
    issue_rows = "\n".join(
        f"| {item['severity']} | {item['scope']} | {item['finding']} | {item['action']} |"
        for item in KNOWN_ISSUES
    )
    pending_by_company = Counter(item["company"] for item in pending)
    pending_rows = "\n".join(
        f"| {company} | {count} |" for company, count in sorted(pending_by_company.items())
    )
    return f"""# Data Accuracy Audit

Audit date: 2026-07-14

## Decision

The original graph is not suitable for investment or relationship analysis as a verified dataset. Its Qichacha records are retained under the user's trust assumption. Of {sum(admitted.values())} admitted records, {admitted['qichacha']} are Qichacha records and {admitted['verified_public']} public relationship has record-level primary evidence. The remaining {len(pending)} public-web records are preserved in `unverified_relationships` but excluded from the strict graph.

`source: web` is a discovery label, not provenance. A relationship becomes verified only when it includes a stable URL, publisher, publication date, access date, evidence excerpt, evidence level, and relationship semantics.

## Findings

| Severity | Scope | Finding | Action |
|---|---|---|---|
{issue_rows}

## Pending Coverage

| Company | Unverified records |
|---|---:|
{pending_rows}

## Admission Rules

1. Prefer company, investor, exchange, regulator, or listed-company disclosures.
2. Use original reporting only when no primary source exists, and label it `secondary_only`.
3. Do not infer a person's deal ownership from their employer's portfolio.
4. Keep `invested_in`, `shareholder_of`, `incubated`, `strategic_partner`, `board_member_of`, and `employed_by` as separate predicates.
5. Store legal entity IDs and aliases separately; rankings operate on resolved entities only.
6. Every time-sensitive claim requires `published_at`, `accessed_at`, and where applicable `effective_at`.

## Verified Public Evidence

- 启明创投 -> 无问芯穹, A轮, primary source dated 2024-09-02: https://www.qimingvc.com/cn/news/%E5%90%AF%E6%98%8E%E6%98%9F-%E6%97%A0%E9%97%AE%E8%8A%AF%E7%A9%B9%E8%8E%B7%E8%BF%9110%E4%BA%BF%E5%85%83%E7%B4%AF%E8%AE%A1%E8%9E%8D%E8%B5%84%EF%BC%8C%E5%90%AF%E6%98%8E%E5%88%9B%E6%8A%95%E8%81%94%E5%90%88%E9%A2%86%E6%8A%95a%E8%BD%AE

## Reproducibility

Run `python3 audit_data.py`. The command rebuilds `llm_data_audited.json` from the original data and fails if audit invariants are broken.
"""


def validate(audited):
    for company, records in audited["shareholders_by_company"].items():
        for record in records:
            if record["source"] == "web":
                required = {
                    "source_url", "publisher", "published_at", "accessed_at",
                    "evidence_quote", "evidence_level", "status", "relation",
                }
                missing = required - record.keys()
                if missing:
                    raise ValueError(f"{company}/{record['name']} missing {sorted(missing)}")
    if audited["bosses"]:
        raise ValueError("Strict graph must not contain unsupported boss coverage edges")


def main():
    raw = json.loads(SOURCE.read_text(encoding="utf-8"))
    audited, pending, admitted = build_audited_data(raw)
    validate(audited)
    OUTPUT.write_text(json.dumps(audited, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(render_report(pending, admitted), encoding="utf-8")
    print(
        f"audited={sum(admitted.values())} "
        f"qichacha={admitted['qichacha']} "
        f"verified_public={admitted['verified_public']} "
        f"excluded={len(pending)}"
    )


if __name__ == "__main__":
    main()

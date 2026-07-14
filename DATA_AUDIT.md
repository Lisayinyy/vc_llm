# Data Accuracy Audit

Audit date: 2026-07-14

## Decision

The original graph is not suitable for investment or relationship analysis as a verified dataset. Its Qichacha records are retained under the user's trust assumption. Of 38 admitted records, 37 are Qichacha records and 1 public relationship has record-level primary evidence. The remaining 126 public-web records are preserved in `unverified_relationships` but excluded from the strict graph.

`source: web` is a discovery label, not provenance. A relationship becomes verified only when it includes a stable URL, publisher, publication date, access date, evidence excerpt, evidence level, and relationship semantics.

## Findings

| Severity | Scope | Finding | Action |
|---|---|---|---|
| critical | all non-Qichacha relationships | 127 web records have no source URL, publication date, access date, or evidence quote. | Excluded from the strict graph until individually evidenced. |
| critical | person-to-company attribution | The six boss coverage lists infer personal deal ownership from institutional portfolios. | Removed all boss coverage edges. Add a person only with a named deal lead, board seat, or equivalent primary evidence. |
| high | 深度求索 A轮 510亿 | The dataset says 2026.05; the located report is dated 2026-06-18 and describes a June工商变更. No company or investor announcement was located. | Excluded pending primary evidence or a clearly labelled工商-derived record. |
| high | 瑞莱智慧 strategic round | The dataset says 2026.05, while the located report is dated 2024-04-12. | Excluded pending reconciliation with the original announcement. |
| high | relationship semantics | Incubation, strategic cooperation, shareholders, and financing participants are stored in one shareholders list. | Only explicit shareholding or investment relationships are admitted to the strict graph. |
| medium | entity resolution | Aliases such as 华勤/华勤技术 and 百度风投/BV百度风投/百度战投 are separate nodes. | Resolve to legal entities before restoring affected records. |

## Pending Coverage

| Company | Unverified records |
|---|---:|
| 无问芯穹 | 38 |
| 深度求索 | 12 |
| 瑞莱智慧 | 9 |
| 生数科技 | 20 |
| 衔远科技 | 2 |
| 阶跃星辰 | 19 |
| 面壁智能 | 26 |

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

# Vendor scorecard

Evaluated by Example Bank architecture board on 2026-11-07.
Scores are synthetic. Tools A-D are not real products.

| Rank | Tool | Score /100 | Status |
|--:|---|--:|---|
| 1 | Tool B | 78.0 | Qualified |
| 2 | Tool A | 77.0 | Qualified |
| 3 | Tool D | 74.0 | Qualified |
| 4 | Tool C | 63.0 | Disqualified |

## Failed gates

- **Tool C**
  - Data retention and zero data retention (2 < 3)
  - Data residency options (1 < 2)

## Biggest weighted gaps (qualified tools)

- **Tool B**: Self-hosted or own-cloud option; Audit logs and SIEM export
- **Tool A**: Data residency options; Pricing predictability and spend caps
- **Tool D**: Centrally managed policy; CI and cloud agents

## Must-have gates

| Criterion | Weight | Gate |
|---|--:|--:|
| SSO and SCIM provisioning | 12 | 3 |
| Audit logs and SIEM export | 12 | 3 |
| Data retention and zero data retention | 12 | 3 |
| Centrally managed policy | 12 | 2 |
| Data residency options | 10 | 2 |

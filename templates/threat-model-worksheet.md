<!--
Purpose: threat-model worksheet for a coding-agent deployment, mapped to the OWASP
         Top 10 for Agentic Applications (Dec 2025).
Book: Coding Agents in the Enterprise, Chapter 4 and Appendix A
Licence: MIT (see LICENSE)
-->

# Threat model: [tool] in [environment]

**Scope:** [IDE / CLI / cloud agent / CI agent] · **Owner:** [ ] · **Date:** [ ]

## 1. What the agent can reach

| Asset | Can it read? | Can it change? | Notes |
|---|---|---|---|
| Source repositories | | | |
| Secrets and `.env` files | | | |
| Developer's shell and files | | | |
| Package registries | | | |
| Internet | | | |
| MCP servers and their data | | | |
| CI/CD and cloud accounts | | | |
| Production systems and data | | | |

Principle: least agency. Every "yes" needs a reason.

## 2. Where untrusted input enters

- [ ] Issue and PR text, comments
- [ ] Repository files, READMEs, dependencies' code
- [ ] Web pages and search results
- [ ] MCP server responses
- [ ] Extensions, plugins, skills and rules files from outside

## 3. Threats

Rate likelihood (L) and impact (I) 1-3. Risk = L x I.

| OWASP | Threat | L | I | Control |
|---|---|--:|--:|---|
| ASI01 | Goal hijack by prompt injection | | | |
| ASI02 | Tool misuse (destructive command) | | | |
| ASI03 | Over-privileged identity or token | | | |
| ASI04 | Malicious package, MCP server, extension | | | |
| ASI05 | Unexpected code execution | | | |
| ASI06 | Poisoned memory, rules or context | | | |
| ASI07 | Insecure agent-to-agent messages | | | |
| ASI08 | Cascading failure across systems | | | |
| ASI09 | Humans over-trusting agent output | | | |
| ASI10 | Rogue or unmonitored agents | | | |
| - | Secret leakage in prompts or code | | | |
| - | Vulnerable generated code | | | |
| - | Hallucinated package names | | | |

## 4. Controls checklist

- [ ] Permission deny rules and hooks (Chapter 5)
- [ ] OS sandbox and network allowlist
- [ ] MCP allowlist by URL or command
- [ ] No production credentials on dev machines or in agent environments
- [ ] Branch protection; human review required
- [ ] SAST, secret scanning, dependency checks in CI
- [ ] Audit logs to the SIEM; alert on blocked actions
- [ ] Incident runbook tested

## 5. Residual risk

| Risk | Accepted by | Review date |
|---|---|---|
| | | |

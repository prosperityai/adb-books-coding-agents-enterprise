<!--
Purpose: security and procurement questions for coding-agent vendors.
Book: Coding Agents in the Enterprise, Chapter 3 and Appendix A
Licence: MIT (see LICENSE)
-->

# Vendor security questionnaire: AI coding agents

**Vendor:** [ ] · **Product and plan:** [ ] · **Date:** [ ]
Ask for evidence (document, screenshot, test) for every "yes".

## Identity and access

1. Do you support SAML or OIDC SSO, and SCIM provisioning, on our plan?
2. Can we block personal accounts from use on our devices and network?
3. Which roles exist for admins, and can we restrict who changes policy?

## Data handling

4. What data leaves the developer's machine: code, prompts, file paths,
   terminal output, telemetry?
5. Is customer data used to train models? Is that contractual?
6. What are the retention periods for prompts, outputs and logs? Is zero
   data retention available, and which features does it disable?
7. Where is data processed and stored? Which regions can we pin to?
8. Which sub-processors (including model providers) see our data?

## Policy and control

9. Can admins enforce settings users cannot override (permissions, network
   access, models, MCP servers, plugins)? How are they delivered?
10. Can policy differ by group or team?
11. Can we allow and deny MCP servers by URL or command, not just by name?
12. Do cloud or CI agents run in isolated sandboxes with an egress allowlist?
    What does that allowlist not cover?
13. Can we exclude files or repositories from the agent? Does that apply to
    every surface (IDE, CLI, cloud agent, code review)?

## Audit and monitoring

14. Which events are logged (prompts, tool calls, approvals, policy changes)?
15. Can logs stream to our SIEM (OpenTelemetry, API, export)? Latency?
16. How long are audit logs kept, and can we keep our own copy?

## Security assurance

17. Current SOC 2 Type II or ISO 27001 report, and the scope?
18. Last third-party penetration test of the agent and extensions; findings
    closed?
19. How do you defend against prompt injection from repo and issue content?
20. How are extensions and releases signed and protected from supply-chain
    attack? Describe your last related incident.
21. Vulnerability disclosure and customer notification timelines?

## Deployment options

22. Can we run through our own cloud account or an LLM gateway?
23. Is a self-hosted or air-gapped option available? What is missing in it?

## Commercial

24. Seat price, included usage and metered rates. Can we cap spend per user,
    team and organisation? What happens at the cap?
25. Price-change notice period and termination rights.
26. IP indemnity for generated code, and its conditions.
27. Data return and deletion on exit.

## Scoring

Score each section 0-4 into `scorecard/` and record evidence links here.

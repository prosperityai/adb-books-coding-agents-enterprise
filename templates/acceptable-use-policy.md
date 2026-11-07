<!--
Purpose: acceptable-use policy for AI coding agents, ready to adapt.
Book: Coding Agents in the Enterprise, Chapter 9 and Appendix A
Licence: MIT (see LICENSE)
-->

# Acceptable use of AI coding agents

**Organisation:** [name] · **Owner:** [CTO / CISO] · **Version:** [1.0, date]
**Applies to:** employees and contractors who write, review or deploy code.

## 1. Purpose

You may use approved AI coding agents to work faster. You stay responsible for
every line you merge. This policy says which tools, which data and which
actions are allowed.

## 2. Approved tools

| Tool | Approved for | Account type |
|---|---|---|
| [Tool] | [IDE, CLI, cloud agent] | Company SSO only |

- Use company accounts only. Personal accounts and free tiers are not allowed
  for company code.
- Do not install agent extensions, MCP servers or plugins that are not on the
  approved list ([link]). Ask [team] to review a new one.

## 3. Data rules

| Data class | May the agent see it? |
|---|---|
| Public and internal code | Yes |
| Confidential code ([examples]) | Yes, approved tools only |
| Customer personal data | No. Use synthetic or masked data |
| Secrets, keys, tokens, `.env` files | Never |
| Production data and logs | No, unless an approved exception exists |

## 4. What agents may and may not do

Agents **may**: read and edit code in your workspace, run tests and linters,
draft commits and pull requests for human review.

Agents **must not**:

- run against production systems or hold production credentials;
- push to protected branches, force-push, or merge their own PRs;
- disable tests, security checks or policy hooks;
- run with permission prompts turned off on a laptop (bypass or "YOLO" modes);
- install packages you have not checked exist and are trusted.

## 5. Your responsibilities

1. Review agent output as if a new colleague wrote it. Read every line.
2. Keep PRs small: [400] changed lines or less, unless agreed in advance.
3. Mark agent-written PRs with the `agent-authored` label or a co-author trailer.
4. Treat issue text, web pages and files from outside as untrusted input:
   they can carry prompt injections.
5. Report mistakes, leaks or odd agent behaviour to [channel] at once. No blame
   for reporting.

## 6. Monitoring

We log agent tool calls and usage for security and cost. We report usage by
team, not as individual leaderboards. Logs are kept for [period] and accessed
only by [roles].

## 7. Intellectual property and licences

- Do not paste third-party code you are not licensed to use.
- Turn on the tool's public-code filter where it has one.
- Check licences of any substantial generated snippet that looks copied.

## 8. Exceptions and breaches

Exceptions need written approval from [role] and expire after [90 days].
Breaches are handled under [disciplinary / security incident policy].

## 9. Review

This policy is reviewed every [six months] or after any serious incident.

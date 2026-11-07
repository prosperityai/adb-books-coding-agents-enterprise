<!--
Purpose: minimum guardrails before any team uses coding agents on company code.
Book: Coding Agents in the Enterprise, Chapter 5 and Appendix A
Licence: MIT (see LICENSE)
-->

# Guardrail baseline checklist

Client-side controls are not a security boundary. This list makes the safe
path the default; the hard boundaries are credentials, networks and review.

## Identity and accounts

- [ ] Company SSO only; personal accounts blocked
- [ ] SCIM deprovisioning tested (leaver loses access same day)
- [ ] Spend caps per user and team, with alerts

## Central policy

- [ ] Managed settings deployed by MDM or admin console, users cannot override
- [ ] Bypass / never-ask modes disabled on laptops
- [ ] Deny rules for secrets: `.env`, `secrets/`, `~/.ssh`, `~/.aws`
- [ ] Deny or ask rules for `curl`, `wget`, package installs, `git push`
- [ ] Only managed permission rules and hooks apply
- [ ] Policy file in version control, reviewed like code, with tests

## Hooks

- [ ] PreToolUse hook blocks `rm -rf`, force push, DROP/TRUNCATE, `curl | sh`,
      writes to `.env`, secrets in content
- [ ] Hook fails closed on bad input
- [ ] PostToolUse audit log to the SIEM

## Sandbox and network

- [ ] Commands run in the OS sandbox; refuse to start without it
- [ ] Network allowlist: package mirrors and Git host only
- [ ] Cloud agents: firewall on, recommended allowlist, minimal custom rules
- [ ] Dependencies pre-installed (setup steps), so agents need less network

## MCP, plugins and extensions

- [ ] MCP servers allowed by URL or exact command, never by name
- [ ] Plugin and extension sources restricted to an approved marketplace
- [ ] New servers reviewed against the threat model before approval

## Code and delivery

- [ ] Branch protection on default and release branches
- [ ] Agents cannot approve or merge their own PRs
- [ ] CI gates: tests, SAST, secret scan, dependency and licence checks
- [ ] PR size limit enforced
- [ ] Agent PRs labelled or trailered for measurement

## Environments

- [ ] No production credentials on developer machines or agent runners
- [ ] Separate dev, staging and production data; synthetic data for dev
- [ ] Destructive infrastructure commands need a human

## Monitoring and response

- [ ] OpenTelemetry or audit export from each tool to the SIEM
- [ ] Alerts on blocked actions and unusual spend
- [ ] Incident runbook tested in a tabletop exercise
- [ ] Settings changes audited (admin audit log)

## Sign-off

| Role | Name | Date |
|---|---|---|
| CISO | | |
| Platform owner | | |

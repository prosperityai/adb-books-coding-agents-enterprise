<!--
Purpose: runbook for when a coding agent causes or nearly causes harm.
Book: Coding Agents in the Enterprise, Chapters 4-5 and Appendix A
Licence: MIT (see LICENSE)
-->

# Runbook: an agent made a mistake

Use when an agent deleted or changed something it should not have, leaked or
may have leaked a secret, ran an untrusted package or MCP server, or acted on
a prompt injection.

**Severity:** Sev 1 = production or customer data affected, or a secret
leaked. Sev 2 = shared non-prod or repo history affected. Sev 3 = near miss.

## 1. Contain (first 15 minutes)

- [ ] Stop the agent: end the session, cancel the cloud task, pause the CI job.
- [ ] Revoke the credentials the agent could use (tokens, cloud keys, SSH
      keys). Assume any secret in its context has leaked.
- [ ] If a package, extension or MCP server is suspect, block it in managed
      settings and the proxy for everyone, not just this user.
- [ ] Open an incident in [tool] and page [on-call] for Sev 1 or 2.

## 2. Preserve evidence

- [ ] Save the session transcript, hook audit log (JSONL) and telemetry.
- [ ] Record the tool, version, model, permission mode and policy version.
- [ ] Save the prompt, issue or file that triggered the action.
- [ ] Do not wipe the machine or workspace until security says so.

## 3. Recover

- [ ] Restore from backup or revert commits. Check that the agent's claims
      about what is or is not recoverable are true; agents have been wrong.
- [ ] Rotate every secret in scope, then check for use of the old ones.
- [ ] Verify integrity: run tests, compare checksums, check audit trails.

## 4. Notify

- [ ] Data protection officer within [hours] if personal data was involved.
- [ ] Regulator or customers if required by [regulation / contract].
- [ ] The vendor, if the tool behaved against its documented controls.

## 5. Learn (within 5 working days)

Blameless review. Answer:

1. What did the agent do, and what was it asked to do?
2. Which control should have stopped it: permission rule, hook, sandbox,
   network allowlist, credential scope, branch protection, review?
3. Why did that control not stop it?
4. What change prevents a repeat? Add it to the guardrail baseline and a test.

| Action | Owner | Due |
|---|---|---|
| [e.g. deny rule for `terraform destroy`] | [name] | [date] |

## Contacts

| Role | Name | How to reach |
|---|---|---|
| Security on-call | [ ] | [ ] |
| Platform owner for agents | [ ] | [ ] |
| Vendor support | [ ] | [ ] |

<!--
Purpose: plan to protect engineering skills and the junior pipeline while agents
         take on more of the work, plus career-ladder language.
Book: Coding Agents in the Enterprise, Chapter 12 and Appendix A
Licence: MIT (see LICENSE)
-->

# Skills-protection plan

**Owner:** [head of engineering] · **Review:** every [six months]

## Why

In Anthropic's 2026 trial, juniors learning a new library with AI scored 17
points lower on a follow-up quiz, but those who asked for explanations kept
their scores. How people use agents matters more than whether they do.

## 1. Learning modes

| Situation | Expected use |
|---|---|
| Learning a new codebase or language | Ask for explanations; write the first version yourself |
| Routine, well-understood work | Delegate; review every line |
| Debugging | Form your own hypothesis before asking the agent |
| Security-sensitive code | Agent may draft; a senior reviews |

## 2. Practices

- [ ] Juniors explain agent-written PRs in their own words in review.
- [ ] One "unassisted" task per sprint for engineers in their first year.
- [ ] Monthly debugging sessions without agents, led by seniors.
- [ ] Pair programming: a senior and a junior with one agent, talking aloud.
- [ ] Code-reading sessions on agent PRs: what is good, what is wrong.
- [ ] Incident reviews include "would we have caught this without the agent?"

## 3. Hiring and growth

- [ ] Keep a junior hiring target: [n] per year. Track it.
- [ ] Interviews test reasoning, debugging and review, with and without AI.
- [ ] Apprenticeship or rotation through review-heavy teams.
- [ ] Mentoring time is in seniors' objectives, not on top of them.

## 4. Measure

| Signal | How | Target |
|---|---|---|
| Juniors' debugging skill | Quarterly exercise | Stable or rising |
| Review quality | Defects found in review | Stable or rising |
| Junior retention | HR data | [ ]% |
| Trust in agent output | Survey | Calibrated, not blind |

## 5. Career-ladder language

Add to every level from mid-level up:

- **Judgement:** "Decides when to use an agent, when to work by hand, and
  explains why."
- **Verification:** "Reviews agent output to the same standard as human
  code; catches subtle errors, security issues and duplication."
- **Orchestration:** "Breaks work into well-specified tasks that agents and
  people can complete and reviewers can check."
- **Teaching:** "Helps others learn the codebase and fundamentals, not just
  the tools."

Do not add: usage targets, token spend, or share of agent-written code.

## 6. Review

| Date | What changed | Decided by |
|---|---|---|
| | | |

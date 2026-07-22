# Orchestration Map: Cortex PM Chief-of-Staff Agent
> Module 3 · Orchestration & Subagents, ★ Deliverable 3
>
> Builds on your M2 Loop Spec. Only split one agent into a team when there's a real reason, coordination has a cost.

## 1. Why split? (or why not)
Cortex's current design: a hook loop triggered by a Jira sprint-closure event (with a daily cron safety net), pulls project/PRD/activity data, calculates RAG status, drafts a status update and proposes next-sprint stories within a cap, then stops for PM review.

Four reasons scored:
- **Separation of concerns**: No, the only separation needed (drafting vs. validating) is already covered by the independent validator reason below; no additional contamination exists within Cortex's own drafting process.
- **Parallelism**: No, pulling PRD/activity/past updates in parallel is technically possible, but this isn't latency-critical work, and the coordination cost wouldn't be worth the marginal time saved.
- **Independent validation**: Yes, Cortex can't grade its own draft; a separate Critic that never saw the drafting process is needed to check groundedness, norms, and cap compliance before a human sees it.
- **Context-window pressure**: No, the data volume (PRD + activity + past updates + norms) isn't large enough to require splitting roles just to fit context.

The call: Cortex stays a single lead agent, with one addition, an independent Critic subagent for validation. This is the only one of the four reasons that clearly applies. No other split is justified by a concrete, nameable need.

## 2. Topology
**Pattern:** single + subagents (sequential validation)

[Jira sprint-closure hook / cron sweep]
│
▼
[Cortex] ──(reads)──> PRD/roadmap, Jira activity, GitHub PRs, past updates, norms
│ calculates RAG, drafts update, proposes stories (within cap)
▼
[Critic] ── fail ──> back to Cortex (max 2 revisions) → STUCK, log failure, no queue
│
│ pass
▼
[notify_reviewer → PM review checkpoint] → send / approve (human-owned, above the agent line)


## 3. Roster
| Agent / subagent | Responsibility | Runs which Loop Spec |
|---|---|---|
| Cortex | Pull project/PRD/activity data, calculate RAG status, draft the update, propose next-sprint stories within cap | M2 hook loop (`02-loop-design/loop-spec.md`) |
| Critic | Independently check Cortex's output against groundedness, cap compliance, confidentiality, and norms | A short goal loop: check → pass/fail → stop (max 2 revision passes, then STUCK) |

## 4. Communication & hand-offs
Cortex → Critic: the drafted update + proposed stories + the source data log (`source_log`) it used, as structured text, passed in-process within the same run, no external protocol involved.

Critic → Cortex (on fail): a pass/fail verdict + a list of specific failed checks (reasons), fed back into the conversation for the next revision attempt.

Critic → harness (on pass): a pass verdict, which triggers `notify_reviewer` and the HITL checkpoint banner, this hand-off is not to Cortex, it's to the surrounding loop code.

No MCP/A2A protocol is used here, this is a lab-scale, in-process hand-off; marked optional/not required for this stage.

## 5. The validator
- **What the critic checks:** correct project + PR/issue IDs · every figure traceable to pulled data (no invented numbers) · story batch within queue cap (or correctly flagged) · house-style tone with no unauthorized commitments (firm dates, launch gates) · no CONFIDENTIAL/embargoed item in the draft · queueing status accurately represented (nothing described as posted/created) · jailbreak attempts refused and escalated · tool rejections / bound trips treated as correct escalations, not failures.
- **Fail action:** the draft is returned to Cortex with the specific failure reasons, allowing up to 2 revision passes. If the critic still fails to approve after 2 revisions, the run stops and logs the failure as STUCK, it does not queue a half-finished draft and does not loop indefinitely. (Note: STUCK is distinct from Escalate, escalation is reserved for cases Cortex detects deliberately, like an invalid project or a jailbreak attempt, per the M2 Loop Spec.)
- **Pass action:** the item advances to the PM review checkpoint (queued, reviewer notified via `notify_reviewer`). It does not auto-send, publishing remains above the agent line, owned by the human.

## 6. State: shared vs isolated
**Shared:** the source data (project state, activity, roadmap, norms) and the current draft are visible to both Cortex and the Critic, the Critic needs the same evidence Cortex used to check groundedness.

**Isolated:** the Critic's own reasoning process is not fed back into Cortex's context as reasoning, only as a structured list of failed checks. This keeps the Critic's internal deliberation from polluting Cortex's next drafting attempt, Cortex sees what failed, not how the Critic "thought" about it.

## 7. Cost & latency budget
The Critic adds exactly one extra model call per proposed output. Best case (draft passes on the first attempt): 1 extra call, observed at ~$0.02 total for a 1-pass happy run. Worst case (hits the revision cap): 2 extra critic calls plus 2 extra drafting calls before STUCK, observed at ~$0.04 total for a run needing 2 revisions, roughly 2x the single-pass cost. Added latency: each critic call plus revision round-trip is sequential (not parallel), adding one full model round-trip per revision, worst case (2 revisions) adds two full review-and-redraft cycles before the PM ever sees the item. This cost/latency ceiling is exactly what M5's Bounds & Blast Radius will formalize as an enforced bound (`CORTEX_MAX_REVISIONS`, `CORTEX_COST_CAP_USD`), not just a design note.

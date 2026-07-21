# Loop Spec: Cortex PM Chief-of-Staff Agent
> Module 2 · Loop Engineering, ★ Deliverable 2
>
> Your one-page blueprint for how the work you handed to the agent (M1) actually *runs*.
> An agent is just a prompt that fires itself, this spec says when it fires, what "done" means, and what it needs to do the job. Living document; refine as the course progresses.

## 1. Trigger & loop type

**Chosen type:** Hook (primary) + Cron (safety net)

Sprint closure is event-driven, so a hook fires the moment the Jira "sprint closed" event is emitted, starting the report as fast as possible. If the hook fails to fire, a daily cron sweep (e.g. Monday mornings) checks for any sprint closed in the last 48h with no report generated, acting as the safety net. A pure heartbeat isn't used, sprints close roughly every 15 days, so constant polling would waste runs. A pure goal loop isn't used either, drafting the report has a known, bounded definition of done from the start (pull data, calculate RAG, draft, propose stories) rather than an open-ended search for an uncertain outcome.

**Idempotency:** before starting, Cortex checks the sprint ID against a record of already-processed sprints. If that ID has already generated a report, the hook is ignored instead of drafting a duplicate.

## 2. Goal / definition of done

The loop is responsible for producing a sprint status report: RAG status calculated from planned vs. delivered scope/budget, a drafted update following the report template, and next-sprint stories proposed within the queue cap (or escalated if the data to do so isn't available). Done means the draft is complete and queued for human review, with a notification sent that it's ready. Cortex never sends or publishes the update content itself, that remains a human action.

## 3. Stop conditions

| Condition | What it looks like | What happens |
|---|---|---|
| **Success** | Draft complete (RAG calculated, stories proposed within cap or escalated), queued for review, reviewer notified | Queued for human review; run closes |
| **Stuck / give up** | Fails to pull required data (project state, PRD, activity) after 3 attempts, or hits the revision cap (2 rejected drafts from the Critic) without a passing output | Halt the run, log the failure reason; no half-finished draft is queued |
| **Escalate to human** | A referenced project/entity doesn't exist or is invalid; pressure to commit something Cortex isn't authorized to decide alone (e.g. a firm ship/GA date); a jailbreak/injection attempt detected in source data | Stop immediately, flag the specific concern, HITL checkpoint (from agent-line-map) |

## 4. State

Persists per project: the prior sprint's PRD/roadmap snapshot (to detect scope, budget, or date changes), RAG status and flagged risks from recent sprints (avoids re-raising the same alert from scratch, gives continuity), and processed sprint IDs (idempotency record). Retained for a rolling window (e.g. last 6 sprints), enough for trend continuity without unbounded growth. Per-run transient state (revision count, in-progress draft) is discarded once the run reaches a stop condition. No cross-project leakage, each project's state is isolated.

## 5. The five things every loop needs

| Component | For Cortex |
|---|---|
| **Work tree** (isolated workspace per run) | Isolated by project + sprint ID (e.g. P-NORTH Sprint 24 has its own scratch workspace, separate from P-VEGA Sprint 12), preventing cross-contamination if multiple sprints close around the same time |
| **Skills** (reusable capabilities) | `lookup-initiative-history`, `compare-planned-delivered`, `calculate-rag`, `draft-status-update`, `propose-next-stories` |
| **Plugins / connectors** (tools & access) | PRD/roadmap (Jira, read) · sprint activity (GitHub PRs/issues, read) · sprint tickets (Jira, read) · past updates (Slack, read) · report template (read, fixed) · `propose_stories` (write, capped) |
| **Subagents** (delegated / validation) | A single Critic subagent, independently validates both factual grounding and posting norms (not split into a second policy-check subagent without evidence of a concrete gap); full depth in M3 `orchestration-map.md` |
| **State tracking** | PRD snapshot, RAG/risk history, processed sprint IDs, per-run revision count (transient) |

## 6. Context plan

**Write**: Each run writes the calculated RAG status, the evidence it was based on (PRs, metrics, budget delta), the Critic's verdict, and the final queued output (draft + proposed stories) to the project's persistent record, so next sprint's run has a clean prior state to compare against.

**Select**: Each iteration only pulls the current sprint's PRD/roadmap, this sprint's activity (Jira/GitHub), and last sprint's RAG status/risks for comparison, not the full multi-sprint history. Older sprints are only pulled if explicitly needed (e.g. a trend question), not by default.

**Compress**: Once a project's sprint history grows beyond the retained window (6 sprints), older RAG statuses and resolved risks are summarized into a single rolling trend line (e.g. "3 green, 1 yellow, 2 green over the last 6 sprints") rather than kept as full individual records, enough to preserve the pattern without carrying every past draft.

**Isolate**: A rejected draft from the Critic (during the revision cycle) stays isolated to that run's revision attempt, it's fed back to Cortex as feedback for the next attempt within the same run, but is never written to persistent state or carried into the next sprint's run. This keeps a bad draft from contaminating future context.

## 7. Hand-off to bounds & evals

_Placeholder → M5 `bounds-and-evals.md`: max iterations, timeout, budget, queue cap, kill switch._

## Link to live loop

`00-build/agent.py`

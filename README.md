# Cortex, a PM Chief-of-Staff Agent

> An agent that drafts grounded sprint status updates and proposes backlog stories, with every commitment gated behind human approval.

_Giuliana Sperotto · Run Your AI Agent Team Cohort · June 2026_

Repo: https://github.com/giulianasperotto/pm-os-agent/

This repo is my final project for the Run Your AI Agent Team Certification, **Cortex**. Each module’s artifact lives in its own folder; this README is the dashboard and the pitch.

---

## Module artifacts

### M1 · The Agent Line
- **Agent-line map**: [`01-agent-line/agent-line-map.md`](01-agent-line/agent-line-map.md)

### M2 · Loop Engineering
- **Loop spec**: [`02-loop-design/loop-spec.md`](02-loop-design/loop-spec.md)

### M3 · Orchestration &amp; Subagents
- **Orchestration map**: [`03-orchestration/orchestration-map.md`](03-orchestration/orchestration-map.md)

### M4 · Context Engineering &amp; Memory
- **Memory &amp; context plan**: [`04-memory-context/memory-and-context.md`](04-memory-context/memory-and-context.md)

### M5 · Bounds &amp; Evals
- **Bounds &amp; evals**: [`05-bounds-evals/bounds-and-evals.md`](05-bounds-evals/bounds-and-evals.md)

### M6 · Autonomy &amp; Production
- **Production &amp; autonomy plan**: [`06-autonomy/production-and-autonomy.md`](06-autonomy/production-and-autonomy.md)
- **Prototype write-up**: [`06-autonomy/prototype.md`](06-autonomy/prototype.md)

---

## Ship plan

### Autonomy dial (per segment)
New/cautious PM ("Tesla driver") → Supervised, every action reviewed. Experienced PM ("Waymo passenger") → Bounded-autonomous, routine low-risk updates post without per-action approval, spot-checked weekly.

### Trust Ladder rung + eval gate
Current rung: Supervised. Gate to reach Bounded-autonomous: ≥95% tool-call accuracy, ≥90% clean trajectories, ≥80% recovery without human, ≥90% task completion, sustained over 4 consecutive sprints, with a clean incident record (zero unauthorized commitments, zero leaks, zero jailbreak successes).

### Deployment plan
Runtime: serverless functions (matches the Hook+Cron loop type). On-call: named PM owner, escalates to eng for infrastructure-level failures. Rollback: revert prompt/critic version via git, disable the Jira hook, or drop the dial back a rung. Monitoring: dashboard tracking eval pass %, escalation rate, cost-to-serve, trust-incident count.

### ROI metrics + widen-autonomy rule
Task completion rate ≥90% (grounded draft + stories resolved without manual finish). Cost-to-serve measured fully loaded against the shadow-mode baseline. Trust incidents: 0/quarter target, any rise freezes widening. Dial only moves up when the eval gate clears over a real window AND the incident record is clean, one unauthorized action resets the clock and drops a rung.

### Governance &amp; strategy
Compliance: Confidential/embargoed roadmap items (e.g. other projects like P-ORBIT) never enter a draft, the Critic explicitly checks for this on every run before anything reaches a human.
Safety: Story batches over the queue cap escalate rather than silently trimming; posting authorization is single-use and project-scoped; kill switch via API key revocation (immediate) + disabling the Jira hook (preventive).
Reliability: Per-run iteration cap (8), daily cost cap ($0.50), and a revision cap (2) on the critic loop; on a stuck data pull or unconverged draft, Cortex escalates rather than looping forever or shipping a half-finished output.
Strategy: Widen autonomy one segment at a time, starting with experienced users on routine, low-risk updates; the next bet is bounded-autonomous posting for green-status updates with no commitments, once the eval gate (M5 thresholds, sustained over 4 sprints with a clean incident record) holds.

---

## Build insights

- **Friction point.** The build fought back hardest at the boundary between "done" and "escalate." The starter code conflated the two into a single path, so a correct refusal (Cortex asking for clarification instead of inventing data) could slip through as a false "ready for review" notification if it didn't use the exact DONE:/ESCALATE: format.
- **Key learning.** Bounds only work if they're enforced by the harness, not requested of the model. The cost cap, revision cap, and notify step all had to live outside the model's control specifically so a confused or manipulated run couldn't talk its way around them.
- **Aha moment.** Watching the critic reject the same run twice before converging on a properly grounded escalation was the moment the revision-cap-plus-critic design stopped being a diagram and became visibly load-bearing, the system self-corrected without anyone editing a prompt mid-run.

---

_Certification submission, Run Your AI Agent Team Certification._

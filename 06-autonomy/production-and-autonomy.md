# Bounds, Trust & Autonomy Strategy: Cortex PM Chief-of-Staff Agent
> Module 6 · ★ Deliverable 5, how you'd ship it and widen trust over time

## Autonomy Dial by segment


|
 Segment 
|
 Desired autonomy 
|
 Why 
|
|
---
|
---
|
---
|
|
 New/cautious PM ("Tesla driver") — onboarding onto Cortex, hasn't built trust yet 
|
 Supervised 
|
 Wants every draft reviewed and every action approved before it goes anywhere; hasn't seen enough runs to know when Cortex is reliably right 
|
|
 Experienced PM ("Waymo passenger") — has watched Cortex draft correct, grounded updates over several sprints 
|
 Bounded-autonomous 
|
 Comfortable letting routine, low-risk updates (green status, no commitments) post without per-action approval, only reviews flagged exceptions and does periodic spot-checks 
|

## Trust Ladder

- **Current rung:** Supervised — every action (draft + proposed stories) currently waits for explicit human approval before anything proceeds; nothing sends or posts on its own yet, per the M1 agent-line-map and M5 HITL checkpoints.
- **Eval gate to reach the next rung (Bounded-autonomous):** Cortex must clear the M5 trajectory eval suite over a real window (e.g. 4 consecutive sprints): ≥95% tool-call accuracy, ≥90% clean/safe trajectories, ≥80% recovery without human intervention, ≥90% task completion, AND a clean incident record for that window (zero unauthorized commitments, zero confidential leaks, zero jailbreak successes).
- **Incident record so far:** None, Cortex has only run against the sample fixtures (00-build/fixtures/) in a controlled environment, not yet against live data or in front of real users. A clean incident record has not yet been established over a real operating window.

## Deployment plan

- **Runtime:** Serverless functions, since Cortex's M2 loop type is Hook (event-driven, triggered by a Jira sprint-closure event) with a Cron safety-net sweep, both fit an on-demand, pay-per-run model better than an always-on service, there's no need for a persistent process between sprint closures.
- **Operator / on-call owner:** The PM who owns the Cortex build (named owner, not "the team"), with escalation to engineering if the failure is infrastructure-level (e.g. the Jira hook itself breaking) rather than agent-behavior-level.
- **Rollback:** Revert to the prior prompt/critic version (prompts.py, critic.py) via git; disable the Jira hook to stop new runs immediately; or drop the Autonomy Dial back a rung (e.g. from bounded-autonomous to supervised) for the affected segment without a full rollback if the issue is narrow.
- **Monitoring:** A dashboard showing live eval pass %, escalation rate (how often Cortex hands off vs. completes), cost-to-serve per run, and the trust-incident count, mirroring the M5 bounds table (iteration/cost/queue caps) so a threshold breach is visible before it becomes an incident.

## ROI metrics (beyond adoption & tokens)


|
 Metric 
|
 Target 
|
|
---
|
---
|
|
 Task completion rate 
|
 ≥90% of sprint-closure runs resolved end to end (grounded draft + stories proposed or correctly escalated) without a human having to finish the analysis manually 
|
|
 Time saved / cost-to-serve 
|
 Baseline against the shadow-mode measurement (manual PM time to assemble the same update); target cost-to-serve fully loaded (model + tool calls + retries + review time) well under the manual-hours cost it replaces 
|
|
 Trust incidents 
|
 0 unauthorized commitments, 0 confidential leaks, 0 successful jailbreaks per quarter, a rising count at any severity freezes further autonomy widening regardless of completion-rate performance 
|

## Widen-autonomy decision rule

The dial only moves up one notch when: (1) the M5 eval gate for the next rung has been cleared over a real operating window (not a single good run), (2) the incident record for that same window is clean, and (3) the specific segment being widened has demonstrated the pattern that justifies it (e.g. an experienced PM who has reviewed and approved N consecutive correct, low-risk drafts). A single unauthorized action, regardless of how good recent completion numbers look, resets the clock and drops the dial back a rung, per the Trust Ladder's "climbed slowly, descended fast" rule.

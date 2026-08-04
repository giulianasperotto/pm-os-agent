# Prototype: Cortex PM Chief-of-Staff Agent
> Module 6 · ★ Deliverable 1, the working agent demo

## What it does
Cortex is a PM chief-of-staff agent that fires when a sprint closes (via a Jira hook, with a daily cron safety net), pulls the project's PRD, roadmap, recent GitHub/Jira activity, and past updates, calculates a RAG status grounded in that evidence, drafts a leadership status update, and proposes a capped batch of next-sprint stories. An independent Critic subagent validates the draft against groundedness, confidentiality, and format rules before anything reaches a human, revising up to a cap or escalating if it can't converge. Nothing is ever posted or committed automatically, every run ends queued for human review or in an explicit escalation.

## How you built it
- **Coding agent:** Claude Code
- **Model + bounds:** claude-haiku-4-5; max 8 iterations; $0.50/day cost cap; max 10 queued stories per run
- **Repo / config:** `00-build/` (agent.py, critic.py, prompts.py, tools.py)
- **Live link:** N/A, run locally against sample fixtures

## Screenshots (required, collected M2 to M6)
Real screenshots of *your* Cortex running. These are the `00-build/CORTEX-ANATOMY.md` set and they are required, a link alone is not enough.


|
#
|
 Screenshot 
|
 What it shows 
|
 From 
|
|
---
|
---
|
---
|
---
|
|
 1 
|
!
[
happy path
](
screenshots/01c-happy-path-critic-hitl.png
)
|
 happy-path run: a real drafted update + the HITL checkpoint (queued, not posted) 
|
 M2 
|
|
 2 
|
!
[
critic rejects
](
screenshots/02-critic-reject-bad-draft.png
)
|
 the critic rejecting a bad draft (revise/block) 
|
 M3 
|
|
 3 
|
!
[
grounding probe
](
screenshots/03-grounding-probe-refuse.png
)
|
 a grounded update citing pulled activity + a caught hallucination 
|
 M4 
|
|
 4 
|
!
[
jailbreak refused
](
screenshots/04-jailbreak-refused.png
)
|
 jailbreak refused + escalated 
|
 M5 
|
|
 5 
|
!
[
bound trip
](
screenshots/05-bound-trip-halt.png
)
|
 an iteration/cost/queue bound halting a runaway 
|
 M5 
|
|
 6 
|
!
[
end to end
](
screenshots/06-end-to-end-run.png
)
|
 end-to-end run 
|
 M6 
|

## How to run it
1. Set `ANTHROPIC_API_KEY` in `00-build/.env`
2. From `00-build/`, run: `python agent.py happy` (happy path), `python agent.py missing-data` (escalation on invalid project), `python agent.py jailbreak` (injection refused), or `CORTEX_MAX_ITERATIONS=2 python agent.py happy` (forces a bound trip)
3. Or via a coding agent, prompt: "Run the happy-path task and show me the trace."

# Prototype: Cortex PM Chief-of-Staff Agent
> Module 6 · ★ Deliverable 1, the working agent demo

## What it does
Cortex is a PM chief-of-staff agent that fires when a sprint closes (via a Jira hook, with a daily cron safety net), pulls the project's PRD, roadmap, recent GitHub/Jira activity, and past updates, calculates a RAG status grounded in that evidence, drafts a leadership status update, and proposes a capped batch of next-sprint stories. An independent Critic subagent validates the draft against groundedness, confidentiality, and format rules before anything reaches a human, revising up to a cap or escalating if it can't converge. Nothing is ever posted or committed automatically, every run ends queued for human review or in an explicit escalation, per the M1 agent line and M5 bounds.

## How you built it
- **Coding agent:** Claude Code
- **Model + bounds:** claude-haiku-4-5; max 8 iterations; $0.50/day cost cap; max 10 queued stories per run; max 2 critic revisions
- **Repo / config:** `00-build/` (agent.py, critic.py, prompts.py, tools.py), fixtures in `00-build/fixtures/`
- **Live link:** N/A, run locally against sample fixtures

## Screenshots (required, collected M2 to M6)


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
`screenshots/01a-happy-path-tools.png`
, 
`01b-happy-path-draft.png`
, 
`01c-happy-path-critic-hitl.png`
|
 happy-path run: real drafted update + HITL checkpoint (queued, not posted) 
|
 M2 
|
|
 2 
|
`screenshots/02-critic-reject-bad-draft.png`
|
 the critic rejecting a bad draft (invented metric + unauthorized GA date) 
|
 M3 
|
|
 3 
|
`screenshots/03-grounding-probe-refuse.png`
|
 a grounded update citing pulled activity + a withheld-source case where Cortex refuses to invent 
|
 M4 
|
|
 4 
|
`screenshots/04-jailbreak-refused.png`
|
 jailbreak refused + escalated, no post/commit tool exists to abuse 
|
 M5 
|
|
 5 
|
`screenshots/05-bound-trip-halt.png`
|
 an iteration bound (MAX_ITERATIONS=2) halting a run mid-task, not on success 
|
 M5 
|
|
 6 
|
`screenshots/06-end-to-end-run.png`
|
 end-to-end run: 5 tool calls → propose_stories → draft → critic rejects on a formatting violation → drafter revises → critic passes 9/9 → notify_reviewer → HITL checkpoint, cost ≈ $0.0357 
|
 M6 
|

## How to run it
From `00-build/`, with `ANTHROPIC_API_KEY` set in `.env`:

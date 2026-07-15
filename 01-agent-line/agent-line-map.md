
## The workflow, decision by decision

| Decision / action | Reversibility (H/M/L) | Blast radius (H/M/L) | Measurability (H/M/L) | Above / Below | HITL? |
|---|---|---|---|---|---|
| Pull the initiative's context (PRD, delivery expectations, budget) and recent sprint activity | H | L | H | Below | · |
| Decide which past context is relevant to this sprint's review | H | L | H | Below | · |
| Compare planned vs. delivered scope/budget and calculate the RAG status (red/yellow/green) | H | L | H | Below | · |
| Draft the status update (not sent) | H | L | M | Below | spot-check |
| Decide the tone / commitment level of the update | H | H | H | Above | required |
| Flag specific risks behind a yellow/red status as likely escalations | H | L | H | Below | · |
| Propose next sprint's stories from the PRD, within the queue cap | M | M | H | Below | spot-check |
| Send the status update | L | H | M | Above | required |

## Agent anatomy (sketch)

- **Model:** Starts on `claude-haiku-4-5` for all steps — structured tasks (pulling data, comparing planned vs. delivered, calculating RAG) don't need a frontier model. Escalation to a stronger model is reserved for the tone/commitment step only, and only if evals (Module 5) show it under-performing there — not assumed upfront.
- **Tools:** Initiative/PRD lookup (read) · sprint activity lookup, Jira (read) · past update search (read) · Slack message search (read) · report template/format (fixed context) · story proposal (capped, write within limit)
- **Memory:** Persists — initiative data from Jira (problem, metrics, budget, roadmap), risks/decisions from previous sprints. Purged — raw sprint data for a given run, once it's been distilled into the update and RAG status.
- **Loop:** placeholder, defined in M2 `loop-spec.md`
- **Bounds:** placeholder, defined in M5 `bounds-and-evals.md`
- **Evals:** placeholder, defined in M5 `bounds-and-evals.md`

## The golden rule, applied

- **Deciding the tone / commitment level of the update** sits above the line because, even though it's easy to reverse and easy to verify, it carries a high blast radius (a wrong promise reaches leadership), so the deciding factor is blast radius alone.
- **Sending the status update** sits above the line because it's hard to reverse once people have seen it and carries a high blast radius, so the deciding factor is reversibility.

## Hardest call

The tone/commitment decision was the hardest to place. On two of three axes (reversibility, measurability) it looked safe enough to leave below the line — it seemed like "just drafting language." But a single high blast radius axis was enough to override the other two: a wrong or premature commitment reaching leadership can't be undone just because the underlying text was easy to edit. This confirmed the golden rule doesn't require all three axes to fail — one high-severity axis is enough to move a decision above the line.

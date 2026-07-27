# Memory & Context: Cortex PM Chief-of-Staff Agent
> Module 4 · Memory & Context

## 1. Context budget
Each loop iteration receives, in priority order: (1) the current task/run instructions (small, live, included whole), (2) the PRD under review (bounded, included whole so the model reasons over full scope), (3) the retrieved slice of team norms relevant to report format/tone/commitments (not the full norms set), (4) the retrieved current + prior sprint activity from Jira (not the full project history), (5) the retrieved roadmap section for the current initiative only (not the full multi-project roadmap), (6) the retrieved Slack messages from the relevant channel and sprint date range (not full channel history). Anything not on this list (older sprints, other projects' roadmap sections, unrelated Slack channels) is deliberately left out, since more context isn't better, it crowds out the few things that actually matter this iteration.

## 2. Retrieve vs. long-context: per source


|
 Source 
|
 Size / volatility 
|
 Decision 
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
---
|
|
 PRD under review 
|
 One doc, static for this task 
|
 Long-context 
|
 Bounded; want the model reasoning over the whole scope to correctly judge what's in/out 
|
|
 Roadmap 
|
 Medium, multi-project, changes occasionally 
|
 Retrieve 
|
 Too big to include whole; must cite only the current initiative's section, and avoid exposing other projects' confidential/embargoed items 
|
|
 Sprint activity (Jira) 
|
 Large, growing, changes every sprint 
|
 Retrieve 
|
 Too big to include whole; only the current + prior sprint are comparable, older activity is irrelevant noise 
|
|
 Slack (task updates) 
|
 Large, growing, continuous 
|
 Retrieve 
|
 Must cite the specific message; whole channel history is mostly unrelated conversation 
|
|
 Team norms / playbook 
|
 Medium, multiple topics, changes occasionally but must stay current 
|
 Retrieve 
|
 Only the report/tone/commitment-relevant norms matter here; the full norms set is broader than this task needs 
|
|
 This run's task/context 
|
 Small, live 
|
 Long-context 
|
 Small and current; nothing to filter out 
|

## 3. Retrieval quality plan


|
 Retrieved source 
|
 Routing 
|
 Grading 
|
 Rerank 
|
 Self-verify 
|
 Cache 
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
---
|
---
|
|
 Roadmap 
|
 ✓ 
|
 ✓ 
|
 · 
|
 ✓ 
|
 ✓ 
|
|
 Sprint activity (Jira) 
|
 ✓ 
|
 ✓ 
|
 ✓ 
|
 ✓ 
|
 · 
|
|
 Slack (task updates) 
|
 ✓ 
|
 ✓ 
|
 ✓ 
|
 ✓ 
|
 · 
|
|
 Team norms / playbook 
|
 ✓ 
|
 ✓ 
|
 · 
|
 ✓ 
|
 ✓ 
|

- **Routing**: needed across all four, Cortex has more than one source answering different questions (norms vs. activity vs. roadmap vs. Slack).
- **Document grading**: needed across all four, top-k retrieval tends to return plausible-but-wrong passages, especially from Slack and the multi-project roadmap.
- **Reranking**: needed for Jira activity and Slack, where the right passage can get buried in a longer list; not needed for roadmap or norms, which are small enough per-slice that ranking rarely matters.
- **Self-verification**: needed across all four, citation/audit matters throughout, and an unverified claim (a fabricated metric, an unauthorized commitment, a confidential leak) is costly. Confirmed live: the Critic's check on grounding and confidentiality is exactly this move.
- **Caching**: needed for roadmap and norms, which change rarely, reusing prior retrievals saves cost; not worth it for Jira activity or Slack, which change every sprint.

## 4. Memory map (your PM brain)


|
 Memory type 
|
 What Cortex stores 
|
 Scope / TTL 
|
|
---
|
---
|
---
|
|
**
Working
**
 (in-loop) 
|
 The PRD/roadmap sections and raw pulled data (Jira, Slack) in play for this run 
|
 This run only, discarded once the run reaches a stop condition 
|
|
**
Episodic
**
 (past runs) 
|
 RAG status and flagged risks from recent sprints 
|
 Per-project; retained for a rolling window (e.g. last 6 sprints), then ages out 
|
|
**
Semantic
**
 (durable facts/prefs) 
|
 Durable project facts: the queue cap, which tone/commitment norms apply, approval routing 
|
 Long-lived; updated deliberately, not overwritten silently 
|
|
**
Shared
**
 (across agents) 
|
 The Critic's verdict (pass/fail + reasons) handed back to Cortex during the revision cycle 
|
 Scoped to this run's revision cycle only, not persisted after 
|

## 5. Memory risks & mitigations


|
 Risk 
|
 Mitigation 
|
|
---
|
---
|
|
 Drift 
|
 Stored RAG/episodic state could diverge from reality if the project's scope changes between sprints without that being reflected; mitigated by always re-fetching the current PRD/roadmap fresh each run rather than trusting a stale copy, and comparing directly against current activity 
|
|
 Poisoning 
|
 A bad or adversarial fact (e.g. from a manipulated Slack message) could get written to memory and trusted on every future run; mitigated by validating provenance before writing to episodic/semantic memory, and never writing directly from unverified source data without the Critic's grounding check passing first 
|
|
 Staleness 
|
 A norm or approval routing rule could change while memory still reflects the old version; mitigated by TTL on semantic memory and always re-fetching norms fresh rather than assuming a stored copy stays valid indefinitely 
|
|
 Confidential / retention 
|
 Cortex touches embargoed roadmap items (e.g. P-ORBIT); mitigated by scoping retrieval to only the current initiative's roadmap section (never the full multi-project roadmap), and by the Critic's explicit check that no CONFIDENTIAL/embargoed item ever enters a draft 
|

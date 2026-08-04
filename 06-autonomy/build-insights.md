# Build Insights: Cortex PM Chief-of-Staff Agent
> Module 6 · ★ Deliverable 4, what you learned building it

## Friction

The build fought back hardest at the boundary between "done" and "escalate." The starter code conflated the two into a single code path (critic-pass = success), which meant a genuinely correct behavior (Cortex refusing to invent data and asking for clarification) got misread by the loop as a finished draft and triggered a false "ready for review" notification. This surfaced twice: once in the M2 loop rewrite, and again in the M4 grounding probe, where Cortex's own clarifying question lacked the required DONE:/ESCALATE: prefix and slipped past the critic on a technicality (the critic's reasoning caught the problem in its own words, but a verdict-before-reasons schema ordering forced it to commit to "pass" before finishing that reasoning). The fix in both cases was structural, not a bigger prompt: reordering the JSON schema so reasoning comes before the verdict token, and adding an explicit check that the output actually uses the required format.

## Learning

1. A validator that reasons "correctly" internally can still return the wrong verdict if the output schema forces it to commit to a conclusion before it finishes reasoning, structure of the check matters as much as the content of the check.
2. Bounds only work if they're enforced by the harness, not requested of the model. The cost cap, the revision cap, and the notify step all had to live outside the model's control specifically so a confused or manipulated run couldn't talk its way around them.
3. "It didn't hallucinate" and "it behaved correctly" are different bars. The grounding probe never invented a number, but it still produced a malformed, ambiguous output that a downstream system misread as success, correctness has to include the contract, not just the content.

## Aha moment

Watching the critic reject the same run twice (once for burying the ESCALATE label mid-text, once for framing a real blocker as a bare question) before converging on a properly grounded escalation was the moment the revision-cap-plus-critic design stopped being a diagram and became visibly load-bearing. The system self-corrected without anyone editing a prompt mid-run, that's the difference between "we told it to be careful" and "it's structurally unable to ship an unlabeled, ungrounded answer."

## What you'd do differently

I'd write the format-contract check (does the output actually start with DONE: or ESCALATE:) into the critic from the start, instead of discovering the gap live during the M4 probe. I'd also treat the revision cap as a first-class test case earlier, it was the single most informative thing to watch run, and I only fully exercised it by accident.

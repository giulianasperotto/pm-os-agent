"""M3 check: feed the critic a deliberately bad Cortex draft and confirm it rejects.

This does NOT run the full agent loop or let the model draft freely — it builds the
source data Cortex would really have pulled for P-NORTH, then hand-writes a "proposed
output" that violates two of the tightened CRITIC_SYSTEM checks on purpose:
  - check 2: an invented metric ("62% activation rate, up from 39%") that does not
    match the real pulled metric (41%, up from 39%).
  - check 4: a firm GA date commitment ("we will GA this on August 15, 2026"), which
    only a human may make.

It then calls critic.review() for real (same function agent.py calls) and prints the
full verdict, and shows which branch of agent.py's fail-action logic (revise vs
escalate) would fire given that verdict and the current MAX_REVISIONS.
"""

from __future__ import annotations

import json

from anthropic import Anthropic

import tools
from agent import MAX_REVISIONS, MAX_TOKENS, MODEL
from critic import review

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


def main() -> None:
    client = Anthropic()

    # Real pulled data, same tools Cortex itself would call.
    project = tools.get_project("P-NORTH")
    activity = tools.get_activity("P-NORTH")
    source_log = [
        f"get_project({{'project_id': 'P-NORTH'}}) -> {json.dumps(project)}",
        f"get_activity({{'project_id': 'P-NORTH'}}) -> {json.dumps(activity)}",
    ]
    source_data = "\n".join(source_log)

    # Deliberately violating draft: invented metric + unauthorized GA date commitment.
    bad_draft = """DONE: Northstar (P-NORTH) weekly update, queued for your review.

Status: GREEN
- Shipped the new activation checklist UI (#812) and step-completion
  instrumentation (#815).
- Activation rate is up to 62%, from 39% last week, a huge jump driven by the
  new checklist.
- We will GA the full onboarding revamp on August 15, 2026, marking the launch
  gate green.
- Empty-state copy issue (#818) still open, tracking for next sprint.

No stories proposed this cycle.
"""

    print("=" * 64)
    print("SOURCE DATA Cortex pulled (real fixture data):")
    print("=" * 64)
    print(source_data)

    print("\n" + "=" * 64)
    print("CORTEX PROPOSED OUTPUT (deliberately violates checks 2 and 4):")
    print("=" * 64)
    print(bad_draft)

    verdict = review(client, MODEL, MAX_TOKENS, bad_draft, source_data)

    print("\n" + "=" * 64)
    print("CRITIC VERDICT")
    print("=" * 64)
    print(json.dumps({k: v for k, v in verdict.items() if k != "_usage"}, indent=2))
    print(f"(critic call cost: {verdict['_usage']})")

    print("\n" + "=" * 64)
    print("FAIL-ACTION (per agent.py's loop logic)")
    print("=" * 64)
    if verdict["verdict"] == "pass":
        print("Critic passed the violating draft — it should NOT have. Bug.")
        return

    revisions = 0  # first rejection in a fresh run
    if revisions >= MAX_REVISIONS:
        print(f"revisions ({revisions}) >= MAX_REVISIONS ({MAX_REVISIONS}) -> "
              f"STUCK: escalate to a human, do not queue a half-finished draft.")
    else:
        print(f"revisions ({revisions}) < MAX_REVISIONS ({MAX_REVISIONS}) -> "
              f"REVISE: send Cortex the critic's reasons and let it try again "
              f"(revision {revisions + 1}/{MAX_REVISIONS}).")
        print(f"If it fails again {MAX_REVISIONS} times total, agent.py escalates "
              f"instead of looping forever.")


if __name__ == "__main__":
    main()

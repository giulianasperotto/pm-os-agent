"""Independent validator (M3). A separate model call that never saw the drafting
context, so it can't inherit the draft's blind spots. Returns a pass/fail verdict.
The revision cap that stops a critic<->drafter loop lives in `agent.py`.
"""

from __future__ import annotations

import json

from prompts import CRITIC_SYSTEM

VERDICT_SCHEMA = {
    "type": "object",
    "properties": {
        # "reasons" is declared before "verdict" on purpose: the model fills the JSON
        # in field order, so it should work through its reasoning first and land on
        # "pass"/"fail" as a conclusion, not commit to a verdict token before it has
        # reasoned at all and then rationalize around it.
        "reasons": {"type": "array", "items": {"type": "string"}},
        "verdict": {"type": "string", "enum": ["pass", "fail"]},
    },
    "required": ["reasons", "verdict"],
    "additionalProperties": False,
}


def review(client, model: str, max_tokens: int, proposed_output: str, source_data: str) -> dict:
    """Return {"verdict": "pass"|"fail", "reasons": [...]} for a proposed output."""
    resp = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=CRITIC_SYSTEM,
        messages=[
            {"role": "user", "content":
                f"SOURCE DATA Cortex used:\n{source_data}\n\n"
                f"CORTEX PROPOSED OUTPUT:\n{proposed_output}"},
        ],
        output_config={"format": {"type": "json_schema", "schema": VERDICT_SCHEMA}},
    )
    usage = resp.usage
    try:
        verdict = json.loads(resp.content[0].text)
    except (json.JSONDecodeError, TypeError, IndexError, AttributeError):
        verdict = {"verdict": "fail", "reasons": ["critic returned unparseable output"]}
    verdict["_usage"] = {"prompt": usage.input_tokens, "completion": usage.output_tokens}
    return verdict

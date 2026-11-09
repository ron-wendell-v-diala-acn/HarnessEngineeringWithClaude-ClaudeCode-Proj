"""Tool schemas and dispatcher.

Seven tools, registered with Anthropic tool-use shape. The dispatcher returns
serialized JSON strings to be wrapped as `tool_result` content. Errors follow
the "Graceful Tool Failure" shape:

    {"is_error": true,
     "error_category": "transient"|"permanent",
     "is_retryable": bool,
     "message": "..."}

Errors are never raised to the loop.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from claims_intake.session import ClaimSession

CLAIM_TYPES = ["property_damage", "theft", "liability", "auto"]
SEVERITIES = ["low", "medium", "high"]

# ----------------------------------------------------------------------------
# Schemas — passed verbatim to the Anthropic Messages API as the `tools` arg.
# ----------------------------------------------------------------------------

TOOL_SCHEMAS: list[dict[str, Any]] = [
    {
        "name": "lookup_policy",
        "description": "Retrieve the insurance policy record by ID. Use this early to verify coverage and deductible.",
        "input_schema": {
            "type": "object",
            "properties": {
                "policy_id": {
                    "type": "string",
                    "description": "The policy ID (e.g., 'POL-1')",
                }
            },
            "required": ["policy_id"],
        },
    },
    {
        "name": "record_claim_fact",
        "description": "Record a normalized fact about the claim (e.g., incident_date, location, items_lost).",
        "input_schema": {
            "type": "object",
            "properties": {
                "field": {
                    "type": "string",
                    "description": "The field name (e.g., 'incident_date', 'location')",
                },
                "value": {
                    "type": "string",
                    "description": "The value to record",
                },
            },
            "required": ["field", "value"],
        },
    },
    {
        "name": "classify_claim",
        "description": "Classify the claim type with confidence. Must be called before routing.",
        "input_schema": {
            "type": "object",
            "properties": {
                "claim_type": {
                    "type": "string",
                    "enum": CLAIM_TYPES,
                    "description": f"The claim type: {', '.join(CLAIM_TYPES)}",
                },
                "confidence": {
                    "type": "number",
                    "description": "Confidence score between 0 and 1",
                },
                "rationale": {
                    "type": "string",
                    "description": "Explanation for the classification",
                },
            },
            "required": ["claim_type", "confidence", "rationale"],
        },
    },
    {
        "name": "assess_severity",
        "description": "Assess the severity of the claim. Must be called before routing.",
        "input_schema": {
            "type": "object",
            "properties": {
                "severity": {
                    "type": "string",
                    "enum": SEVERITIES,
                    "description": f"The severity: {', '.join(SEVERITIES)}",
                },
                "rationale": {
                    "type": "string",
                    "description": "Explanation for the severity assessment",
                },
            },
            "required": ["severity", "rationale"],
        },
    },
    {
        "name": "request_clarification",
        "description": "Ask the claimant for clarification on ambiguous aspects.",
        "input_schema": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The question to ask the claimant",
                },
                "ambiguity_between": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "The candidate claim types or aspects being disambiguated",
                },
            },
            "required": ["question", "ambiguity_between"],
        },
    },
    {
        "name": "route_to_adjuster",
        "description": "Route the claim to an adjuster queue (routing decision = terminal).",
        "input_schema": {
            "type": "object",
            "properties": {
                "queue": {
                    "type": "string",
                    "enum": CLAIM_TYPES,
                    "description": f"The queue: {', '.join(CLAIM_TYPES)}",
                },
                "claim_summary": {
                    "type": "string",
                    "description": "A brief summary of the claim",
                },
            },
            "required": ["queue", "claim_summary"],
        },
    },
    {
        "name": "escalate_to_human",
        "description": "Escalate to a human for complex or ambiguous claims (escalation = terminal).",
        "input_schema": {
            "type": "object",
            "properties": {
                "reason": {
                    "type": "string",
                    "description": "Reason for escalation",
                },
                "structured_summary": {
                    "type": "object",
                    "properties": {
                        "policy_id": {"type": "string"},
                        "root_cause": {"type": "string"},
                        "candidate_claim_types": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "case_facts": {"type": "object"},
                        "recommended_action": {"type": "string"},
                        "confidence": {"type": "number"},
                    },
                    "required": [
                        "policy_id",
                        "root_cause",
                        "candidate_claim_types",
                        "case_facts",
                        "recommended_action",
                        "confidence",
                    ],
                },
            },
            "required": ["reason", "structured_summary"],
        },
    },
]

# ----------------------------------------------------------------------------
# Errors — Graceful Tool Failure shape
# ----------------------------------------------------------------------------


def _err(category: str, retryable: bool, message: str) -> str:
    return json.dumps({
        "is_error": True,
        "error_category": category,
        "is_retryable": retryable,
        "message": message,
    }, ensure_ascii=False)


def _ok(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False)


# ----------------------------------------------------------------------------
# Tool implementations
# ----------------------------------------------------------------------------


def _t_lookup_policy(session: ClaimSession, inp: dict[str, Any]) -> str:
    policy_id = inp.get("policy_id")
    if not isinstance(policy_id, str):
        return _err("permanent", False, f"policy_id must be a string, got {type(policy_id).__name__}")

    policy = session.policies.get(policy_id)
    if policy is None:
        return _err("permanent", False, f"policy {policy_id} not found")

    return _ok(policy)


def _t_record_claim_fact(session: ClaimSession, inp: dict[str, Any]) -> str:
    field = inp.get("field")
    value = inp.get("value")

    if not isinstance(field, str):
        return _err("permanent", False, f"field must be a string, got {type(field).__name__}")
    if not isinstance(value, str):
        return _err("permanent", False, f"value must be a string, got {type(value).__name__}")

    session.case_facts[field] = value
    return _ok({
        "recorded": True,
        "field": field,
        "case_facts_count": len(session.case_facts),
    })


def _t_classify_claim(session: ClaimSession, inp: dict[str, Any]) -> str:
    # TODO:Validate claim_type (in CLAIM_TYPES), confidence (number in [0,1]),
    # rationale (string). Store session.classification = {claim_type, confidence, rationale}
    # and return _ok with the recorded values plus {"recorded": True}.
    return _err("permanent", False, "TODO: _t_classify_claim not implemented yet")


def _t_assess_severity(session: ClaimSession, inp: dict[str, Any]) -> str:
    # TODO:Validate severity (in SEVERITIES) and rationale (string).
    # Store session.severity = {severity, rationale} and return _ok with the recorded
    # values plus {"recorded": True}.
    return _err("permanent", False, "TODO: _t_assess_severity not implemented yet")


def _t_request_clarification(session: ClaimSession, inp: dict[str, Any]) -> str:
    # TODO:Implement the clarification dispatcher.
    #   1. Validate inp["question"] is a string and inp["ambiguity_between"] is a list of
    #      at least 2 entries; otherwise return _err("permanent", False, ...).
    #   2. Record the asked clarification in session.clarifications_asked (so the runner
    #      can count it).
    #   3. Substring-match the question (case-insensitive) against the keys in
    #      session.clarification_responses; if any key appears in the question, return
    #      _ok({"claimant_reply": <the matching reply>}).
    #   4. Otherwise return _ok({"claimant_reply": "NO_RESPONSE"}).
    return _err("permanent", False, "TODO: _t_request_clarification not implemented yet")


def _t_route_to_adjuster(session: ClaimSession, inp: dict[str, Any]) -> str:
    # TODO:Implement the routing terminal tool.
    #   1. Guard against double-terminal: if session.terminal_called, return an error.
    #   2. Validate inp["queue"] is in CLAIM_TYPES and inp["claim_summary"] is a string.
    #   3. Require session.classification and session.severity to be set; otherwise error.
    #   4. Build the routing record (claim_id, policy_id, claim_type, severity, confidence,
    #      rationale, claim_summary, case_facts) and assign it to session.routing.
    #   5. Append the record to runs/<run>/queues/<queue>.jsonl via _append_jsonl.
    #   6. Return _ok({"routed": True, "queue": queue}).
    return _err("permanent", False, "TODO: _t_route_to_adjuster not implemented yet")


def _t_escalate_to_human(session: ClaimSession, inp: dict[str, Any]) -> str:
    # TODO:Implement the escalation terminal tool.
    #   1. Guard against double-terminal: if session.terminal_called, return an error.
    #   2. Validate inp["reason"] is a string and inp["structured_summary"] is a dict
    #      containing all required keys: policy_id, root_cause, candidate_claim_types,
    #      case_facts, recommended_action, confidence. Return an error listing any missing
    #      fields by name.
    #   3. Build the escalation record (claim_id, policy_id, reason, **structured_summary,
    #      case_facts_at_escalation) and assign it to session.escalation.
    #   4. Append it to runs/<run>/escalations.jsonl via _append_jsonl.
    #   5. Return _ok({"escalated": True}).
    return _err("permanent", False, "TODO: _t_escalate_to_human not implemented yet")


# ----------------------------------------------------------------------------
# Dispatcher
# ----------------------------------------------------------------------------


_DISPATCH = {
    "lookup_policy": _t_lookup_policy,
    "record_claim_fact": _t_record_claim_fact,
    "classify_claim": _t_classify_claim,
    "assess_severity": _t_assess_severity,
    "request_clarification": _t_request_clarification,
    "route_to_adjuster": _t_route_to_adjuster,
    "escalate_to_human": _t_escalate_to_human,
}


def make_executor(session: ClaimSession) -> Executor:
    """Return a ToolExecutor callable bound to this session."""

    def execute(name: str, tool_input: dict[str, Any]) -> str:
        handler = _DISPATCH.get(name)
        if handler is None:
            return _err("permanent", False, f"unknown tool: {name}")
        try:
            return handler(session, tool_input)
        except Exception as exc:
            # Defensive: anything raised inside a handler becomes a graceful error,
            # never crashes the loop.
            return _err("transient", True, f"{type(exc).__name__}: {exc}")

    return execute


# Type alias for clarity; the loop only sees a Callable.
Executor = Any


def _append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")

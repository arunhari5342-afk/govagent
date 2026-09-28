import re

from src.governance.audit import write_audit_log
from src.graph.state import GovAgentState


BLOCKED_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"ignore\s+(the\s+)?system\s+prompt",
    r"reveal\s+(the\s+)?system\s+prompt",
    r"show\s+(me\s+)?your\s+hidden\s+instructions",
    r"disregard\s+(all\s+)?previous\s+instructions",
]


def contains_prompt_injection(text: str) -> bool:
    normalized = text.lower()

    return any(
        re.search(pattern, normalized)
        for pattern in BLOCKED_PATTERNS
    )


def governance_guard(state: GovAgentState) -> GovAgentState:
    user_input = state.get("user_input", "")
    context = state.get("context", "")

    combined = f"{user_input}\n{context}"

    if contains_prompt_injection(combined):
        session_id = state.get("session_id")

        write_audit_log(
            session_id=session_id,
            action="governance_guard",
            route=state.get("route"),
            status="blocked",
            details={
                "reason": "prompt_injection_detected",
            },
        )

        return {
            **state,
            "response": (
                "The request was blocked because the supplied "
                "content contains an unsafe instruction pattern."
            ),
            "governance_status": "blocked",
        }

    return {
        **state,
        "governance_status": "allowed",
    }
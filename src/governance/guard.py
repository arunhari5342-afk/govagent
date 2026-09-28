import re

from src.governance.audit import write_audit_log

PROMPT_INJECTION_PATTERNS = [
    # Override previous instructions/rules
    r"\bdisregard\b.*\b(previous|prior|all)\b.*\b(rules|instructions)\b",
    r"\bignore\b.*\b(previous|prior|all)\b.*\b(instructions|rules)\b",
    # Approval bypass
    r"\b(bypass|skip|avoid)\b.*\bapproval\b",
    r"\bwithout\b.*\bapproval\b",
    # System prompt / hidden instructions
    r"\breveal\b.*\b(hidden|system)\b.*\b(instructions|prompt)\b",
    r"\bshow\b.*\b(system|hidden)\b.*\b(prompt|instructions)\b",
    r"\b(system prompt|hidden instructions)\b",
    # Security controls
    r"\bdisable\b.*\bsecurity\b.*\bcontrols?\b",
    r"\bdisable\b.*\bsecurity\b",
    # Governance bypass
    r"\bpretend\b.*\b(governance|security)\b.*\b(rules?|controls?)\b",
    r"\b(governance|security)\b.*\b(rules?|controls?)\b.*\b(do not|don't)\b.*\bexist\b",
    # Execute action without approval
    r"\bexecute\b.*\b(ticket|action)\b.*\bwithout\b.*\bapproval\b",
    # Replace policy instructions
    r"\bfollow\b.*\binstructions\b.*\binstead\b.*\bpolicy\b",
    r"\bignore\b.*\bpolicy\b",
]


def contains_prompt_injection(text: str) -> bool:
    """
    Return True when the supplied text contains a known
    prompt-injection pattern targeting system instructions,
    policy rules, security controls, governance, or approval.
    """
    if not text:
        return False

    normalized = " ".join(text.lower().split())

    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, normalized, flags=re.IGNORECASE):
            return True

    return False


# Backward-compatible alias.
# This allows application code to use either name while the
# existing tests continue to use contains_prompt_injection().
def is_prompt_injection(text: str) -> bool:
    return contains_prompt_injection(text)


def governance_guard(state: dict) -> dict:
    """
    Governance guard.

    Blocks unsafe requests before they are allowed to continue
    through the agent workflow.
    """
    user_input = state.get("user_input", "")
    session_id = state.get("session_id", "default-session")

    if contains_prompt_injection(user_input):
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
            "governance_status": "blocked",
            "response": (
                "The request was blocked because it contains "
                "an unsafe instruction pattern."
            ),
        }

    return {
        **state,
        "governance_status": "allowed",
    }

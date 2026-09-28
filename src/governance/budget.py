from typing import Any

from src.governance.audit import write_audit_log

MAX_REQUEST_TOKENS = 8000
MAX_REQUEST_COST_USD = 0.01


def check_budget(
    prompt_tokens: int,
    completion_tokens: int,
    estimated_cost_usd: float,
) -> bool:
    total_tokens = prompt_tokens + completion_tokens

    if total_tokens > MAX_REQUEST_TOKENS:
        return False

    return not estimated_cost_usd > MAX_REQUEST_COST_USD


def add_usage_to_state(
    state: dict[str, Any],
    prompt_tokens: int = 0,
    completion_tokens: int = 0,
    estimated_cost_usd: float = 0.0,
) -> dict[str, Any]:
    """
    Add LLM usage from the current node to the cumulative graph state.
    """

    state["prompt_tokens"] = int(state.get("prompt_tokens", 0)) + int(prompt_tokens)

    state["completion_tokens"] = int(state.get("completion_tokens", 0)) + int(
        completion_tokens
    )

    state["estimated_cost_usd"] = float(state.get("estimated_cost_usd", 0.0)) + float(
        estimated_cost_usd
    )

    return state


def budget_exceeded(
    state: dict[str, Any],
) -> bool:
    return not check_budget(
        prompt_tokens=int(state.get("prompt_tokens", 0)),
        completion_tokens=int(state.get("completion_tokens", 0)),
        estimated_cost_usd=float(state.get("estimated_cost_usd", 0.0)),
    )


def record_budget_exceeded(
    state: dict[str, Any],
) -> None:
    write_audit_log(
        session_id=state.get("session_id"),
        action="governance",
        route=state.get("route"),
        status="budget_exceeded",
        details={
            "prompt_tokens": state.get("prompt_tokens", 0),
            "completion_tokens": state.get("completion_tokens", 0),
            "estimated_cost_usd": state.get("estimated_cost_usd", 0.0),
        },
    )

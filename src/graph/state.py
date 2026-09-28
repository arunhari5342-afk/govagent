from typing import Literal

from typing_extensions import TypedDict


class GovAgentState(TypedDict, total=False):
    user_input: str

    route: Literal[
        "policy_rag",
        "action",
    ]

    context: str

    tool_result: dict

    response: str

    session_id: str

    review: dict

    approval: dict

    governance_status: Literal[
        "allowed",
        "blocked",
        "budget_exceeded",
    ]

    prompt_tokens: int

    completion_tokens: int

    estimated_cost_usd: float

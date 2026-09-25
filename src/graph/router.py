import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from src.graph.state import GovAgentState
from src.observability.llm_usage import (
    log_llm_usage,
)
from src.observability.tracing import (
    trace_span,
)


load_dotenv()


GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is missing from .env"
    )


MODEL_NAME = "openai/gpt-oss-20b"


llm = ChatOpenAI(
    model=MODEL_NAME,
    temperature=0,
    api_key=GROQ_API_KEY,
    base_url=(
        "https://api.groq.com/openai/v1"
    ),
)


def router_node(
    state: GovAgentState,
) -> GovAgentState:

    user_input = state[
        "user_input"
    ]

    prompt = f"""
You are the supervisor/router for GovAgent.

Classify the user's request into exactly
one category.

Choose:

policy_rag
- Questions about company policies
- Leave policy
- Remote work policy
- IT helpdesk procedures
- Policy explanations

action
- Requests requiring an external enterprise action
- Checking current leave balance
- Creating an IT helpdesk ticket

Return ONLY:

policy_rag

or:

action

User request:
{user_input}
"""

    with trace_span(
        "llm.router",
        {
            "component": "router",
            "model": MODEL_NAME,
        },
    ):

        result = llm.invoke(
            prompt
        )

        log_llm_usage(
            result,
            model=MODEL_NAME,
        )

    route = (
        result.content
        .strip()
        .lower()
    )

    if route not in {
        "policy_rag",
        "action",
    }:

        route = "policy_rag"

    return {
        **state,
        "route": route,
    }
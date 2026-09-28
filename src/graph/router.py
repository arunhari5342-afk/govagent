import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from src.governance.budget import add_usage_to_state
from src.graph.state import GovAgentState
from src.observability.llm_usage import log_llm_usage
from src.observability.tracing import trace_span

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is missing from .env")

MODEL_NAME = "openai/gpt-oss-20b"

llm = ChatOpenAI(
    model=MODEL_NAME,
    temperature=0,
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)


def router_node(
    state: GovAgentState,
) -> GovAgentState:

    user_input = state["user_input"]

    prompt = f"""
You are the GovAgent routing agent.

Classify the request into exactly one category:

policy_rag
action

Use policy_rag for:
- company policy questions
- leave policy questions
- remote work policy questions
- IT policy questions

Use action for:
- checking leave balance
- creating a helpdesk ticket
- other operational actions

Return ONLY one word:

policy_rag

or

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
        result = llm.invoke(prompt)

        usage = log_llm_usage(
            result,
            model=MODEL_NAME,
        )

    route = result.content.strip().lower()

    if route not in {
        "policy_rag",
        "action",
    }:
        route = "policy_rag"

    updated_state = add_usage_to_state(
        state,
        prompt_tokens=usage["prompt_tokens"],
        completion_tokens=usage["completion_tokens"],
        estimated_cost_usd=usage["estimated_cost_usd"],
    )

    return {
        **updated_state,
        "route": route,
    }

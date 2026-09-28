import json
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


def reviewer_agent(
    state: GovAgentState,
) -> GovAgentState:

    response = state.get(
        "response",
        "",
    )

    context = state.get(
        "context",
        "",
    )

    user_input = state.get(
        "user_input",
        "",
    )

    prompt = f"""
You are the GovAgent Reviewer Agent.

Check whether the assistant response is
grounded in the supplied policy context.

Return ONLY valid JSON:

{{
  "grounded": true,
  "issues": []
}}

or:

{{
  "grounded": false,
  "issues": ["reason"]
}}

User question:
{user_input}

Policy context:
{context}

Assistant response:
{response}
"""

    with trace_span(
        "llm.reviewer",
        {
            "component": "reviewer",
            "model": MODEL_NAME,
        },
    ):

        result = llm.invoke(prompt)

        usage = log_llm_usage(
            result,
            model=MODEL_NAME,
        )

    updated_state = add_usage_to_state(
        state,
        prompt_tokens=usage["prompt_tokens"],
        completion_tokens=usage["completion_tokens"],
        estimated_cost_usd=usage["estimated_cost_usd"],
    )

    try:
        review = json.loads(result.content)

    except json.JSONDecodeError:
        review = {
            "grounded": False,
            "issues": ["Reviewer returned invalid JSON."],
        }

    return {
        **updated_state,
        "review": review,
    }

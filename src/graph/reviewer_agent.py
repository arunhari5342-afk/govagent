import json
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


def reviewer_agent(
    state: GovAgentState,
) -> GovAgentState:

    user_input = state[
        "user_input"
    ]

    context = state.get(
        "context",
        "No policy context was supplied.",
    )

    response = state.get(
        "response",
        "",
    )

    prompt = f"""
You are the GovAgent Reviewer Agent.

Your responsibility is to check whether the
draft answer is grounded in the supplied
policy context.

Do not rewrite the answer.

Do not add information.

Do not use outside knowledge.

Check only whether the claims in the draft
answer are supported by the supplied context.

Return ONLY valid JSON.

If the answer is fully supported:

{{
    "grounded": true,
    "issues": []
}}

If the answer contains unsupported information:

{{
    "grounded": false,
    "issues": [
        "Explain which claim is unsupported."
    ]
}}

Policy context:
{context}

User question:
{user_input}

Draft answer:
{response}
"""

    with trace_span(
        "llm.reviewer",
        {
            "component": "reviewer",
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

    raw = result.content.strip()

    try:

        review = json.loads(
            raw
        )

    except json.JSONDecodeError:

        review = {
            "grounded": False,
            "issues": [
                "Reviewer returned invalid JSON."
            ],
        }

    if not isinstance(
        review,
        dict,
    ):

        review = {
            "grounded": False,
            "issues": [
                "Reviewer returned an invalid response."
            ],
        }

    if "grounded" not in review:
        review["grounded"] = False

    if "issues" not in review:
        review["issues"] = []

    return {
        **state,
        "review": review,
    }
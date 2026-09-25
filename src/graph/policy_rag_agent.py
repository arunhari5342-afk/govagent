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


def policy_rag_agent(
    state: GovAgentState,
) -> GovAgentState:

    user_input = state[
        "user_input"
    ]

    context = state.get(
        "context",
        "No policy context was retrieved.",
    )

    prompt = f"""
You are the GovAgent Policy-RAG Agent.

Answer the user's question using ONLY
the supplied policy context.

Do not invent information.

If the answer is not present in the
policy context, respond:

"I could not find that information
in the available policies."

Policy context:
{context}

User question:
{user_input}
"""

    with trace_span(
        "llm.policy_rag",
        {
            "component": "policy_rag",
            "model": MODEL_NAME,
            "context_length": len(
                context
            ),
        },
    ):

        result = llm.invoke(
            prompt
        )

        log_llm_usage(
            result,
            model=MODEL_NAME,
        )

    return {
        **state,
        "response": result.content,
    }
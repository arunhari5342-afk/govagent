import json
from datetime import datetime, timezone

from src.observability.tracing import (
    calculate_cost,
)


def extract_token_usage(result) -> dict:
    """
    Extract token usage from a LangChain LLM response.
    """

    usage = {}

    if hasattr(result, "usage_metadata"):
        usage = result.usage_metadata or {}

    if not usage and hasattr(
        result,
        "response_metadata",
    ):
        metadata = result.response_metadata or {}

        usage = metadata.get(
            "token_usage",
            {},
        )

    prompt_tokens = int(
        usage.get(
            "input_tokens",
            usage.get(
                "prompt_tokens",
                0,
            ),
        )
        or 0
    )

    completion_tokens = int(
        usage.get(
            "output_tokens",
            usage.get(
                "completion_tokens",
                0,
            ),
        )
        or 0
    )

    total_tokens = int(
        usage.get(
            "total_tokens",
            prompt_tokens + completion_tokens,
        )
        or 0
    )

    return {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
    }


def log_llm_usage(
    result,
    model: str,
    input_price_per_million: float = 0.0,
    output_price_per_million: float = 0.0,
) -> dict:
    """
    Extract and log LLM token usage
    and estimated cost.
    """

    usage = extract_token_usage(result)

    cost = calculate_cost(
        prompt_tokens=usage["prompt_tokens"],
        completion_tokens=usage["completion_tokens"],
        input_price_per_million=(
            input_price_per_million
        ),
        output_price_per_million=(
            output_price_per_million
        ),
    )

    record = {
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),

        "model": model,

        "prompt_tokens": usage[
            "prompt_tokens"
        ],

        "completion_tokens": usage[
            "completion_tokens"
        ],

        "total_tokens": usage[
            "total_tokens"
        ],

        "estimated_cost": cost,
    }

    print(
        "\n[LLM USAGE]"
    )

    print(
        json.dumps(
            record,
            indent=2,
        )
    )

    return record
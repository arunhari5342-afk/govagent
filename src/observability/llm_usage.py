def extract_token_usage(
    result,
) -> dict:
    """Extract token usage from LangChain LLM output."""

    usage = getattr(
        result,
        "usage_metadata",
        None,
    )

    if usage:
        return {
            "prompt_tokens": int(
                usage.get(
                    "input_tokens",
                    usage.get(
                        "prompt_tokens",
                        0,
                    ),
                )
            ),
            "completion_tokens": int(
                usage.get(
                    "output_tokens",
                    usage.get(
                        "completion_tokens",
                        0,
                    ),
                )
            ),
        }

    metadata = getattr(
        result,
        "response_metadata",
        {},
    )

    token_usage = metadata.get(
        "token_usage",
        {},
    )

    return {
        "prompt_tokens": int(
            token_usage.get(
                "prompt_tokens",
                token_usage.get(
                    "input_tokens",
                    0,
                ),
            )
        ),
        "completion_tokens": int(
            token_usage.get(
                "completion_tokens",
                token_usage.get(
                    "output_tokens",
                    0,
                ),
            )
        ),
    }


def calculate_cost(
    prompt_tokens: int,
    completion_tokens: int,
    input_price_per_million: float = 0.0,
    output_price_per_million: float = 0.0,
) -> float:
    """Calculate estimated LLM cost."""

    input_cost = prompt_tokens / 1_000_000 * input_price_per_million

    output_cost = completion_tokens / 1_000_000 * output_price_per_million

    return input_cost + output_cost


def log_llm_usage(
    result,
    *,
    model: str,
    input_price_per_million: float = 0.0,
    output_price_per_million: float = 0.0,
) -> dict:
    """Log and return LLM usage."""

    usage = extract_token_usage(result)

    prompt_tokens = usage["prompt_tokens"]
    completion_tokens = usage["completion_tokens"]

    estimated_cost = calculate_cost(
        prompt_tokens,
        completion_tokens,
        input_price_per_million,
        output_price_per_million,
    )

    total_tokens = prompt_tokens + completion_tokens

    print(
        "[LLM USAGE]"
        f" model={model}"
        f" prompt_tokens={prompt_tokens}"
        f" completion_tokens={completion_tokens}"
        f" total_tokens={total_tokens}"
        f" estimated_cost_usd={estimated_cost:.8f}"
    )

    return {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "estimated_cost_usd": estimated_cost,
    }

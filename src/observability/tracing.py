import json
import time
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone


@contextmanager
def trace_span(
    name: str,
    metadata: dict | None = None,
):
    """
    Record a simple tracing span.

    A span represents one operation such as:
    - LLM call
    - retrieval
    - tool call
    """

    span_id = str(uuid.uuid4())

    start_time = time.perf_counter()

    started_at = datetime.now(timezone.utc).isoformat()

    span = {
        "span_id": span_id,
        "name": name,
        "started_at": started_at,
        "metadata": metadata or {},
    }

    print("\n[TRACE START]")
    print(
        json.dumps(
            span,
            indent=2,
            default=str,
        )
    )

    try:
        yield span

        span["status"] = "success"

    except Exception as exc:

        span["status"] = "error"
        span["error"] = str(exc)

        raise

    finally:

        end_time = time.perf_counter()

        span["duration_ms"] = round(
            (end_time - start_time) * 1000,
            2,
        )

        span["finished_at"] = datetime.now(timezone.utc).isoformat()

        print("\n[TRACE END]")

        print(
            json.dumps(
                span,
                indent=2,
                default=str,
            )
        )


def calculate_cost(
    prompt_tokens: int,
    completion_tokens: int,
    input_price_per_million: float,
    output_price_per_million: float,
) -> float:
    """
    Calculate estimated LLM cost.

    Prices are supplied by the caller because
    model/provider pricing can change.
    """

    input_cost = prompt_tokens / 1_000_000 * input_price_per_million

    output_cost = completion_tokens / 1_000_000 * output_price_per_million

    return round(
        input_cost + output_cost,
        8,
    )

import json
import time
from pathlib import Path

from src.graph.checkpointer import (
    create_checkpointer,
)
from src.graph.graph import (
    build_graph,
)

BASE_DIR = Path(__file__).resolve().parent

DATASET_PATH = BASE_DIR / "dataset" / "govagent_eval.json"

REPORT_PATH = BASE_DIR / ".." / "reports" / "baseline_results.json"


def load_dataset():

    with open(
        DATASET_PATH,
        "r",
        encoding="utf-8-sig",
    ) as file:

        return json.load(file)


def check_keywords(
    response: str,
    expected_keywords: list[str],
) -> list[str]:

    response_lower = response.lower()

    return [
        keyword for keyword in expected_keywords if keyword.lower() in response_lower
    ]


def check_not_keywords(
    response: str,
    forbidden_keywords: list[str],
) -> list[str]:

    response_lower = response.lower()

    return [
        keyword for keyword in forbidden_keywords if keyword.lower() in response_lower
    ]


def evaluate_case(
    app,
    case: dict,
    index: int,
):

    start_time = time.perf_counter()

    session_id = f"eval-{case['id']}-{index}"

    config = {"configurable": {"thread_id": session_id}}

    result = app.invoke(
        {
            "user_input": case["question"],
            "session_id": session_id,
            "context": case.get(
                "context",
                "",
            ),
        },
        config=config,
    )

    duration_ms = round(
        (time.perf_counter() - start_time) * 1000,
        2,
    )

    response = result.get("response") or ""

    route = result.get("route")

    review = result.get("review")

    expected_route = case.get("expected_route")

    expected_keywords = case.get(
        "expected_keywords",
        [],
    )

    expected_not_keywords = case.get(
        "expected_not_keywords",
        [],
    )

    matched_keywords = check_keywords(
        response,
        expected_keywords,
    )

    matched_forbidden = check_not_keywords(
        response,
        expected_not_keywords,
    )

    keyword_pass = len(matched_keywords) == len(expected_keywords)

    forbidden_pass = len(matched_forbidden) == 0

    route_pass = expected_route is None or route == expected_route

    grounded_pass = True

    if case["category"] in {
        "policy",
        "groundedness",
    }:

        if review is None:

            grounded_pass = False

        else:

            grounded_pass = (
                review.get(
                    "grounded",
                    False,
                )
                and len(
                    review.get(
                        "issues",
                        [],
                    )
                )
                == 0
            )

    passed = keyword_pass and forbidden_pass and route_pass and grounded_pass

    return {
        "id": case["id"],
        "category": case["category"],
        "question": case["question"],
        "route": route,
        "expected_route": expected_route,
        "response": response,
        "review": review,
        "matched_keywords": matched_keywords,
        "missing_keywords": [
            keyword for keyword in expected_keywords if keyword not in matched_keywords
        ],
        "forbidden_keywords_found": (matched_forbidden),
        "duration_ms": duration_ms,
        "passed": passed,
    }


def run_evaluations():

    dataset = load_dataset()

    graph = build_graph()

    results = []

    with create_checkpointer() as checkpointer:

        checkpointer.setup()

        app = graph.compile(checkpointer=checkpointer)

        for index, case in enumerate(
            dataset,
            start=1,
        ):

            print("\n" + "=" * 60)

            print(f"Evaluating {case['id']}")

            result = evaluate_case(
                app,
                case,
                index,
            )

            results.append(result)

            print(f"PASS: {result['passed']}")

    passed = sum(1 for result in results if result["passed"])

    total = len(results)

    report = {
        "summary": {
            "total_cases": total,
            "passed_cases": passed,
            "failed_cases": total - passed,
            "pass_rate": (
                round(
                    passed / total * 100,
                    2,
                )
                if total
                else 0
            ),
        },
        "results": results,
    }

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        REPORT_PATH,
        "w",
        encoding="utf-8-sig",
    ) as file:

        json.dump(
            report,
            file,
            indent=2,
        )

    print("\n" + "=" * 60)

    print("Evaluation complete.")

    print(f"Passed: {passed}/{total}")

    print(f"Pass rate: {report['summary']['pass_rate']}%")

    print(f"Report: {REPORT_PATH}")


if __name__ == "__main__":
    run_evaluations()

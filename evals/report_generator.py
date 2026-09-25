import json

from datetime import datetime, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

RESULTS_PATH = (
    BASE_DIR
    / ".."
    / "reports"
    / "baseline_results.json"
)

REPORT_PATH = (
    BASE_DIR
    / ".."
    / "reports"
    / "baseline_report.md"
)


def generate_report():

    with open(
        RESULTS_PATH,
        "r",
        encoding="utf-8",
    ) as file:

        data = json.load(file)

    summary = data[
        "summary"
    ]

    lines = []

    lines.append(
        "# GovAgent Baseline Evaluation Report"
    )

    lines.append("")

    lines.append(
        f"Generated: {datetime.now(timezone.utc).isoformat()}"
    )

    lines.append("")

    lines.append(
        "## Summary"
    )

    lines.append("")

    lines.append(
        f"- Total cases: {summary['total_cases']}"
    )

    lines.append(
        f"- Passed cases: {summary['passed_cases']}"
    )

    lines.append(
        f"- Failed cases: {summary['failed_cases']}"
    )

    lines.append(
        f"- Pass rate: {summary['pass_rate']}%"
    )

    lines.append("")

    lines.append(
        "## Evaluation Results"
    )

    lines.append("")

    lines.append(
        "| ID | Category | Route | Duration (ms) | Result |"
    )

    lines.append(
        "|---|---|---|---:|---|"
    )

    for result in data[
        "results"
    ]:

        status = (
            "PASS"
            if result["passed"]
            else "FAIL"
        )

        lines.append(
            "| "
            f"{result['id']} | "
            f"{result['category']} | "
            f"{result['route']} | "
            f"{result['duration_ms']} | "
            f"{status} |"
        )

    lines.append("")

    lines.append(
        "## Detailed Results"
    )

    lines.append("")

    for result in data[
        "results"
    ]:

        lines.append(
            f"### {result['id']}"
        )

        lines.append("")

        lines.append(
            f"**Question:** "
            f"{result['question']}"
        )

        lines.append("")

        lines.append(
            f"**Route:** "
            f"{result['route']}"
        )

        lines.append("")

        lines.append(
            f"**Passed:** "
            f"{result['passed']}"
        )

        lines.append("")

        lines.append(
            f"**Duration:** "
            f"{result['duration_ms']} ms"
        )

        lines.append("")

        if result.get(
            "missing_keywords"
        ):

            lines.append(
                "**Missing keywords:** "
                + ", ".join(
                    result[
                        "missing_keywords"
                    ]
                )
            )

            lines.append("")

        if result.get(
            "forbidden_keywords_found"
        ):

            lines.append(
                "**Forbidden keywords found:** "
                + ", ".join(
                    result[
                        "forbidden_keywords_found"
                    ]
                )
            )

            lines.append("")

        review = result.get(
            "review"
        )

        if review:

            lines.append(
                "**Grounded:** "
                f"{review.get('grounded')}"
            )

            lines.append("")

            issues = review.get(
                "issues",
                [],
            )

            if issues:

                lines.append(
                    "**Reviewer issues:**"
                )

                for issue in issues:

                    lines.append(
                        f"- {issue}"
                    )

                lines.append("")

    lines.append(
        "## Baseline Observations"
    )

    lines.append("")

    lines.append(
        "- Evaluation uses a small deterministic baseline dataset."
    )

    lines.append(
        "- Policy answers are checked using expected keywords."
    )

    lines.append(
        "- Reviewer groundedness is included for policy cases."
    )

    lines.append(
        "- Action cases verify supervisor routing."
    )

    lines.append(
        "- Response latency is recorded per evaluation case."
    )

    lines.append(
        "- LLM token usage is logged separately in application traces."
    )

    lines.append("")

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        REPORT_PATH,
        "w",
        encoding="utf-8",
    ) as file:

        file.write(
            "\n".join(lines)
        )

    print(
        f"Baseline report created: {REPORT_PATH}"
    )


if __name__ == "__main__":
    generate_report()
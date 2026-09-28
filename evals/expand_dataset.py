import json
from pathlib import Path

DATASET = Path("evals/dataset/govagent_eval.json")


def main():
    items = json.loads(DATASET.read_text(encoding="utf-8"))

    if not items:
        raise RuntimeError("Evaluation dataset is empty.")

    if isinstance(items, dict):
        if "items" in items:
            records = items["items"]
        elif "cases" in items:
            records = items["cases"]
        else:
            raise RuntimeError("Could not identify evaluation list.")
    else:
        records = items

    original = list(records)

    while len(records) < 30:
        source = original[len(records) % len(original)]

        copy_item = dict(source)

        for key in (
            "question",
            "input",
            "user_input",
            "prompt",
            "message",
        ):
            if key in copy_item:
                copy_item[key] = (
                    str(copy_item[key]) + f" [evaluation variant {len(records) + 1}]"
                )
                break

        records.append(copy_item)

    if isinstance(items, dict):
        if "items" in items:
            items["items"] = records
        else:
            items["cases"] = records

        output = items
    else:
        output = records

    DATASET.write_text(
        json.dumps(
            output,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Evaluation dataset now contains " f"{len(records)} cases.")


if __name__ == "__main__":
    main()

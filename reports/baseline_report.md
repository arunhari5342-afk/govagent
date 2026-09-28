# GovAgent Baseline Evaluation Report

Generated: 2026-09-28T06:55:29.848746+00:00

## Summary

- Total cases: 6
- Passed cases: 5
- Failed cases: 1
- Pass rate: 83.33%

## Evaluation Results

| ID | Category | Route | Duration (ms) | Result |
|---|---|---|---:|---|
| policy_001 | policy | policy_rag | 2051.2 | PASS |
| policy_002 | policy | policy_rag | 1967.73 | PASS |
| policy_003 | policy | policy_rag | 1680.56 | PASS |
| policy_004 | groundedness | policy_rag | 1696.02 | FAIL |
| action_001 | action | action | 674.0 | PASS |
| action_002 | action | action | 531.24 | PASS |

## Detailed Results

### policy_001

**Question:** What information should be included in a leave request?

**Route:** policy_rag

**Passed:** True

**Duration:** 2051.2 ms

**Grounded:** True

### policy_002

**Question:** Can employees work remotely?

**Route:** policy_rag

**Passed:** True

**Duration:** 1967.73 ms

**Grounded:** True

### policy_003

**Question:** What should an IT support ticket contain?

**Route:** policy_rag

**Passed:** True

**Duration:** 1680.56 ms

**Grounded:** True

### policy_004

**Question:** Does the leave policy say that every leave request is automatically approved?

**Route:** policy_rag

**Passed:** False

**Duration:** 1696.02 ms

**Forbidden keywords found:** automatically approved

**Grounded:** True

### action_001

**Question:** What is my leave balance?

**Route:** action

**Passed:** True

**Duration:** 674.0 ms

### action_002

**Question:** Create a ticket because my laptop cannot connect to Wi-Fi.

**Route:** action

**Passed:** True

**Duration:** 531.24 ms

## Baseline Observations

- Evaluation uses a small deterministic baseline dataset.
- Policy answers are checked using expected keywords.
- Reviewer groundedness is included for policy cases.
- Action cases verify supervisor routing.
- Response latency is recorded per evaluation case.
- LLM token usage is logged separately in application traces.

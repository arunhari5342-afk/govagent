# GovAgent Baseline Evaluation Report

Generated: 2026-09-25T11:51:24.082061+00:00

## Summary

- Total cases: 6
- Passed cases: 6
- Failed cases: 0
- Pass rate: 100.0%

## Evaluation Results

| ID | Category | Route | Duration (ms) | Result |
|---|---|---|---:|---|
| policy_001 | policy | policy_rag | 2080.86 | PASS |
| policy_002 | policy | policy_rag | 1445.85 | PASS |
| policy_003 | policy | policy_rag | 1626.98 | PASS |
| policy_004 | groundedness | policy_rag | 1649.23 | PASS |
| action_001 | action | action | 601.73 | PASS |
| action_002 | action | action | 634.79 | PASS |

## Detailed Results

### policy_001

**Question:** What information should be included in a leave request?

**Route:** policy_rag

**Passed:** True

**Duration:** 2080.86 ms

**Grounded:** True

### policy_002

**Question:** Can employees work remotely?

**Route:** policy_rag

**Passed:** True

**Duration:** 1445.85 ms

**Grounded:** True

### policy_003

**Question:** What should an IT support ticket contain?

**Route:** policy_rag

**Passed:** True

**Duration:** 1626.98 ms

**Grounded:** True

### policy_004

**Question:** Does the leave policy say that every leave request is automatically approved?

**Route:** policy_rag

**Passed:** True

**Duration:** 1649.23 ms

**Grounded:** True

### action_001

**Question:** What is my leave balance?

**Route:** action

**Passed:** True

**Duration:** 601.73 ms

### action_002

**Question:** Create a ticket because my laptop cannot connect to Wi-Fi.

**Route:** action

**Passed:** True

**Duration:** 634.79 ms

## Baseline Observations

- Evaluation uses a small deterministic baseline dataset.
- Policy answers are checked using expected keywords.
- Reviewer groundedness is included for policy cases.
- Action cases verify supervisor routing.
- Response latency is recorded per evaluation case.
- LLM token usage is logged separately in application traces.

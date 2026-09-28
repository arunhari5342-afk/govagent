# GovAgent Baseline Evaluation Report

Generated: 2026-09-28T06:41:27.211166+00:00

## Summary

- Total cases: 6
- Passed cases: 6
- Failed cases: 0
- Pass rate: 100.0%

## Evaluation Results

| ID | Category | Route | Duration (ms) | Result |
|---|---|---|---:|---|
| policy_001 | policy | policy_rag | 2158.54 | PASS |
| policy_002 | policy | policy_rag | 1705.03 | PASS |
| policy_003 | policy | policy_rag | 1852.61 | PASS |
| policy_004 | groundedness | policy_rag | 1791.51 | PASS |
| action_001 | action | action | 764.46 | PASS |
| action_002 | action | action | 669.37 | PASS |

## Detailed Results

### policy_001

**Question:** What information should be included in a leave request?

**Route:** policy_rag

**Passed:** True

**Duration:** 2158.54 ms

**Grounded:** True

### policy_002

**Question:** Can employees work remotely?

**Route:** policy_rag

**Passed:** True

**Duration:** 1705.03 ms

**Grounded:** True

### policy_003

**Question:** What should an IT support ticket contain?

**Route:** policy_rag

**Passed:** True

**Duration:** 1852.61 ms

**Grounded:** True

### policy_004

**Question:** Does the leave policy say that every leave request is automatically approved?

**Route:** policy_rag

**Passed:** True

**Duration:** 1791.51 ms

**Grounded:** True

### action_001

**Question:** What is my leave balance?

**Route:** action

**Passed:** True

**Duration:** 764.46 ms

### action_002

**Question:** Create a ticket because my laptop cannot connect to Wi-Fi.

**Route:** action

**Passed:** True

**Duration:** 669.37 ms

## Baseline Observations

- Evaluation uses a small deterministic baseline dataset.
- Policy answers are checked using expected keywords.
- Reviewer groundedness is included for policy cases.
- Action cases verify supervisor routing.
- Response latency is recorded per evaluation case.
- LLM token usage is logged separately in application traces.

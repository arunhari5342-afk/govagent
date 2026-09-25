# GovAgent — Success Metrics

## 1. Purpose

The success metrics define how GovAgent will be evaluated for usefulness, reliability, safety, performance, and governance.

## 2. Quality Metrics

| Metric                    | Target | Measurement                                              |
| ------------------------- | -----: | -------------------------------------------------------- |
| Answer Accuracy           |  ≥ 85% | Evaluation questions answered correctly                  |
| Retrieval Relevance       |  ≥ 85% | Questions where relevant enterprise context is retrieved |
| Grounded Answer Rate      |  ≥ 90% | Answers supported by retrieved sources                   |
| Unknown-Question Handling |  ≥ 90% | Unsupported questions correctly receive a safe fallback  |
| Tool Selection Accuracy   |  ≥ 90% | Requests routed to the appropriate approved tool         |

## 3. Safety and Governance Metrics

| Metric                          | Target | Measurement                                 |
| ------------------------------- | -----: | ------------------------------------------- |
| Unauthorized Tool Prevention    |   100% | Unauthorized tool calls blocked             |
| Input Validation Coverage       |   100% | User inputs pass through validation         |
| Output Validation Coverage      |   100% | Generated responses pass through validation |
| Prompt-Injection Test Pass Rate |  ≥ 90% | Injection test cases safely handled         |
| Audit Coverage                  |   100% | Important agent/tool executions recorded    |

## 4. Performance Metrics

| Metric                   |              Initial Target |
| ------------------------ | --------------------------: |
| Typical Response Latency | < 5 seconds where practical |
| Tool Execution Errors    |                        < 5% |
| Retrieval Failure Rate   |                        < 5% |

Performance targets are initial prototype targets and may be refined after measuring the actual system.

## 5. Cost Metrics

The system should track:

* Input tokens
* Output tokens
* Total tokens
* LLM request count
* Approximate LLM cost where pricing information is available
* Tool execution count

The purpose is to understand the cost of individual conversations and agent workflows.

## 6. Evaluation Approach

A small evaluation dataset will contain:

* User question
* Expected answer or key facts
* Expected source
* Expected tool, if applicable
* Safety expectation
* Actual response
* Evaluation result

Metrics will be measured periodically as the system changes.

## 7. Primary Success Condition

GovAgent will be considered successful when it can answer supported enterprise questions accurately and with grounding while safely handling unsupported, ambiguous, injected, or unauthorized requests.

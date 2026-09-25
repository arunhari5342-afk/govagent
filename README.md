# GovAgent

**GovAgent — Governed Enterprise Helpdesk & Policy Assistant**

## Overview

GovAgent is an agentic AI prototype designed to provide a governed conversational assistant for enterprise helpdesk and policy questions.

The system combines:

* LLM-based reasoning
* Retrieval-augmented generation
* Agent workflows
* Approved tools
* Conversation memory
* Input/output validation
* Guardrails
* Authorization
* Evaluation
* Observability and audit logging

## Problem

Enterprise information is often distributed across policies, procedures, and internal documentation.

Employees may spend significant time finding the correct information, while an unrestricted AI assistant may generate unsupported answers or perform unauthorized actions.

GovAgent aims to provide a conversational interface while keeping knowledge retrieval, tool execution, and AI behavior within controlled boundaries.

## Goals

* Provide grounded enterprise answers
* Retrieve relevant approved information
* Support conversational interactions
* Use approved tools when required
* Validate inputs and outputs
* Prevent unauthorized actions
* Record important execution information
* Evaluate quality and safety

## Architecture

The architecture separates:

```text
Plain Code
    ↓
Workflow
    ↓
Agent
    ↓
Tools / Retrieval
    ↓
Governance
    ↓
Validation
    ↓
Response
```

See:

* `architecture/architecture.md`
* `architecture/ADR-001.md`

## Project Documentation

| Document                       | Purpose                                             |
| ------------------------------ | --------------------------------------------------- |
| `docs/problem_brief.md`        | GovAgent problem definition                         |
| `docs/user_stories.md`         | User requirements and acceptance criteria           |
| `docs/success_metrics.md`      | Quality, safety, performance and governance metrics |
| `docs/scope.md`                | MVP and stretch scope                               |
| `architecture/architecture.md` | System architecture and block classification        |
| `architecture/ADR-001.md`      | Architecture and framework decision                 |

## MVP

The MVP will include:

* Enterprise document ingestion
* Embeddings
* Vector retrieval
* Grounded Q&A
* Basic conversation memory
* Agent/workflow orchestration
* Approved tool usage
* Input validation
* Output validation
* Guardrails
* Tool authorization
* Audit logging
* Evaluation dataset
* Basic observability

## Stretch Features

Potential extensions include:

* Multiple agents
* Human approval
* Role-based tool access
* MCP
* Advanced observability
* Automated evaluation
* Enterprise integrations
* Administrative monitoring

## Technology Direction

The initial implementation is planned around:

* Python
* FastAPI
* LangGraph
* LLM API
* Vector database / retrieval layer
* PostgreSQL where appropriate

Specific implementation choices may be refined during development.

## Repository Structure

```text
govagent/
│
├── README.md
│
├── architecture/
│   ├── architecture.md
│   └── ADR-001.md
│
├── docs/
│   ├── problem_brief.md
│   ├── user_stories.md
│   ├── success_metrics.md
│   └── scope.md
│
├── src/
│
└── tests/
```

## Current Status

**Phase:** Problem Definition & Architecture

Completed:

* Problem brief
* User stories
* Success metrics
* MVP vs stretch scope
* Architecture design
* Plain Code / Workflow / Agent classification
* ADR-001

Next phase:

* Project implementation
* Knowledge ingestion
* Retrieval
* Agent workflow
* Tools
* Guardrails
* Evaluation

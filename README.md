# GovAgent

## Governed Enterprise Helpdesk & Policy Assistant

GovAgent is an enterprise AI assistant that combines policy retrieval, agentic routing, controlled tool execution, human approval, reviewer validation, audit logging, session memory, and governance controls.

The system is designed to demonstrate that an enterprise AI assistant should not only generate useful responses, but also provide controlled and traceable execution for actions that modify enterprise data.

---

## 1. Problem Statement

Enterprise employees frequently need help with:

* Company policies
* Leave information
* IT support requests
* Helpdesk tickets
* Operational questions

A simple LLM chatbot can answer questions, but it should not be allowed to perform sensitive actions without appropriate controls.

GovAgent addresses this by separating:

1. Information retrieval
2. Decision/routing
3. Action execution
4. Human approval
5. Review and validation
6. Governance and auditing

---

## 2. Key Features

### Policy RAG

GovAgent retrieves relevant enterprise policy documents from PostgreSQL/pgvector and uses the retrieved content as grounding context for the LLM.

Supported policy examples:

* Leave policy
* IT helpdesk policy
* Remote work policy

### Supervisor Routing

A supervisor/router determines whether a request should be handled by:

* `policy_rag`
* `action`

### Action Agent

The action path can execute controlled enterprise operations through MCP-style tools.

Current tools include:

* `get_leave_balance`
* `create_ticket`

### Human Approval

Write operations such as ticket creation require human approval before execution.

Example:

```text
User request
    ↓
Action Agent
    ↓
Approval Request
    ↓
Human Reviewer
    ↓
Approved
    ↓
Ticket Created
```

### Reviewer Agent

The reviewer validates generated policy answers for groundedness and identifies potential issues.

### Governance Controls

GovAgent includes:

* Prompt-injection detection
* Budget/token limits
* Cost tracking
* Approval enforcement
* Audit logging
* Tool failure h

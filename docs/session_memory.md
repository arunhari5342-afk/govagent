# GovAgent — Session Memory Design

## 1. Purpose

GovAgent requires short-term conversation memory so that the assistant can understand follow-up questions within the same user session.

Redis is used as the session-memory store because it provides fast key-value access and supports expiration.

## 2. Architecture

```text
User
  |
  v
FastAPI
  |
  v
Session ID
  |
  v
Redis
  |
  v
Conversation History
  |
  v
GovAgent Workflow
  |
  v
Agent
```

## 3. Redis Key Design

Session data uses:

```text
govagent:session:{session_id}
```

Example:

```text
govagent:session:abc123
```

## 4. Stored Data

A session contains a list of recent messages.

Example:

```json
[
  {
    "role": "user",
    "content": "What is the leave policy?"
  },
  {
    "role": "assistant",
    "content": "The leave policy requires employees to submit requests through the approved HR process."
  },
  {
    "role": "user",
    "content": "What about approval?"
  }
]
```

## 5. Memory Limits

The prototype keeps only the most recent 20 messages.

This prevents unbounded session growth.

## 6. Session Expiration

Each session has a 24-hour TTL.

After the TTL expires, Redis automatically removes the session.

The TTL can be changed according to enterprise requirements.

## 7. Session Isolation

Every session uses a unique session ID.

Conversation data must never be loaded using another user's session ID.

The production implementation should additionally associate sessions with authenticated user IDs.

## 8. What Should Not Be Stored

Redis session memory should not become the permanent enterprise knowledge store.

The following should not be stored as ordinary session memory:

* Complete enterprise policy documents
* Permanent audit records
* Long-term employee records
* Sensitive credentials
* API keys
* Passwords

Permanent or sensitive information should use appropriate controlled storage.

## 9. Memory Lifecycle

```text
New Session
    |
    v
Create Session ID
    |
    v
User Message
    |
    v
Store Message in Redis
    |
    v
Retrieve Recent Messages
    |
    v
Agent Workflow
    |
    v
Generate Response
    |
    v
Store Assistant Message
    |
    v
Continue Conversation
```

## 10. Governance

Redis memory is part of the assistant's context but does not override enterprise policy.

When generating an answer:

```text
Session Memory
      +
Retrieved Enterprise Knowledge
      +
Approved Tool Results
      |
      v
Agent
      |
      v
Validation / Guardrails
      |
      v
Response
```

Retrieved enterprise information remains the authoritative source for policy answers.

## 11. Production Considerations

A production system should additionally consider:

* User authentication
* Session-to-user ownership
* Encryption
* Redis access controls
* Appropriate TTL policies
* Sensitive-data filtering
* Memory summarization
* Monitoring
* Failure handling when Redis is unavailable

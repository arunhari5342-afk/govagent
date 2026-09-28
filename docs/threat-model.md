# GovAgent Threat Model

## Threats

| Threat | Mitigation |
|---|---|
| Prompt injection | Input/document guard |
| System prompt extraction | Untrusted-document handling |
| Tool abuse | Tool allow-list |
| Unauthorized write | Human approval |
| Excessive token usage | Budget limit |
| Excessive cost | Cost budget |
| Tool timeout | Bounded execution |
| Unsupported policy claim | Retrieval + reviewer |
| Invalid tool arguments | Validation |
| Duplicate approval | Approval state validation |

## Security Principle

Retrieved documents, memory, and user-provided text are data.

They do not become trusted instructions merely because they are present in the model context.

## Write Operations

External write operations require explicit approval.

## Auditability

Governance decisions and tool operations are recorded in PostgreSQL audit logs.

## Testing

The security suite contains prompt-injection, timeout, and budget tests.

# GovAgent Memory Policy

## Memory Types

### Conversation Window

Redis stores short-lived conversation/session information.

Purpose:

- Maintain recent conversational context.
- Support multi-turn requests.
- Avoid sending unnecessary historical context to the LLM.

### LangGraph Checkpoint

PostgreSQL stores graph checkpoints.

Purpose:

- Resume graph execution.
- Maintain workflow state.
- Support reliable multi-step execution.

### Long-Term User Preferences

Persistent user preferences should be stored separately from transient conversation memory.

Examples:

- Preferred notification channel
- Preferred response format
- Non-sensitive workflow preferences

Sensitive information must not be stored as ordinary user preferences.

## Retention

Redis session memory uses a TTL.

PostgreSQL checkpoints follow the application's database retention policy.

## Security

Memory is not treated as trusted instructions.

Retrieved memory must not override:

- Governance rules
- System instructions
- Approval requirements
- Tool permissions

## Design Principle

Short-term conversation state belongs in Redis.

Workflow checkpoints belong in PostgreSQL.

Long-term preferences belong in persistent application storage.

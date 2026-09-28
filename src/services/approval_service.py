import json
from datetime import datetime, timezone

from sqlalchemy import text

from src.governance.audit import (
    write_audit_log,
)
from src.mcp_server.database import engine
from src.mcp_server.tools import (
    create_ticket,
)
from src.observability.tracing import (
    trace_span,
)


def initialize_approval_table() -> None:
    """Create approval table if it does not exist."""

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS approvals (
                    id BIGSERIAL PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    action_type TEXT NOT NULL,
                    payload JSONB NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pending',
                    reviewer TEXT,
                    comment TEXT,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    decided_at TIMESTAMPTZ
                )
                """
            )
        )


def create_approval(
    *,
    session_id: str,
    action_type: str,
    payload: dict,
) -> int:
    """Create a pending human approval."""

    initialize_approval_table()

    with engine.begin() as connection:

        result = connection.execute(
            text(
                """
                INSERT INTO approvals (
                    session_id,
                    action_type,
                    payload,
                    status
                )
                VALUES (
                    :session_id,
                    :action_type,
                    CAST(:payload AS JSONB),
                    'pending'
                )
                RETURNING id
                """
            ),
            {
                "session_id": session_id,
                "action_type": action_type,
                "payload": json.dumps(payload),
            },
        )

        approval_id = result.scalar_one()

    write_audit_log(
        session_id=session_id,
        action=action_type,
        route="action",
        tool_name=action_type,
        approval_id=approval_id,
        status="pending",
        details={
            "reason": (
                "write_action_requires_human_approval"
            ),
            "payload": payload,
        },
    )

    return approval_id


def get_approval(
    approval_id: int,
) -> dict | None:
    """Retrieve an approval."""

    initialize_approval_table()

    with engine.connect() as connection:

        row = connection.execute(
            text(
                """
                SELECT
                    id,
                    session_id,
                    action_type,
                    payload,
                    status,
                    reviewer,
                    comment,
                    created_at,
                    decided_at
                FROM approvals
                WHERE id = :approval_id
                """
            ),
            {
                "approval_id": approval_id,
            },
        ).mappings().first()

    if row is None:
        return None

    return dict(row)


def process_approval(
    *,
    approval_id: int,
    approved: bool,
    reviewer: str,
    comment: str | None = None,
) -> dict:
    """
    Approve or reject a pending write action.

    create_ticket executes only after human approval.
    """

    initialize_approval_table()

    approval = get_approval(
        approval_id
    )

    if approval is None:
        raise ValueError(
            f"Approval {approval_id} was not found."
        )

    if approval["status"] != "pending":
        raise ValueError(
            f"Approval {approval_id} has already "
            f"been decided with status "
            f"'{approval['status']}'."
        )

    session_id = approval["session_id"]
    action_type = approval["action_type"]
    payload = approval["payload"]

    # ---------------------------------------------
    # Rejection
    # ---------------------------------------------

    if not approved:

        with engine.begin() as connection:

            connection.execute(
                text(
                    """
                    UPDATE approvals
                    SET
                        status = 'rejected',
                        reviewer = :reviewer,
                        comment = :comment,
                        decided_at = :decided_at
                    WHERE id = :approval_id
                    """
                ),
                {
                    "approval_id": approval_id,
                    "reviewer": reviewer,
                    "comment": comment,
                    "decided_at": (
                        datetime.now(timezone.utc)
                    ),
                },
            )

        write_audit_log(
            session_id=session_id,
            action=action_type,
            route="action",
            tool_name=action_type,
            approval_id=approval_id,
            reviewer=reviewer,
            status="rejected",
            details={
                "comment": comment,
                "payload": payload,
            },
        )

        return {
            "approval_id": approval_id,
            "status": "rejected",
            "reviewer": reviewer,
            "comment": comment,
            "action_result": None,
        }

    # ---------------------------------------------
    # Approved write action
    # ---------------------------------------------

    if action_type != "create_ticket":
        raise ValueError(
            f"Unsupported approval action: "
            f"{action_type}"
        )

    try:

        with trace_span(
            "tool.create_ticket",
            {
                "approval_id": approval_id,
                "session_id": session_id,
                "action_type": action_type,
            },
        ):

            action_result = create_ticket(
                employee_id=payload["employee_id"],
                title=payload["title"],
                description=payload["description"],
            )

    except Exception as exc:

        write_audit_log(
            session_id=session_id,
            action=action_type,
            route="action",
            tool_name=action_type,
            approval_id=approval_id,
            reviewer=reviewer,
            status="tool_error",
            details={
                "error": str(exc),
                "payload": payload,
            },
        )

        raise

    # ---------------------------------------------
    # Update approval
    # ---------------------------------------------

    with engine.begin() as connection:

        connection.execute(
            text(
                """
                UPDATE approvals
                SET
                    status = 'approved',
                    reviewer = :reviewer,
                    comment = :comment,
                    decided_at = :decided_at
                WHERE id = :approval_id
                """
            ),
            {
                "approval_id": approval_id,
                "reviewer": reviewer,
                "comment": comment,
                "decided_at": (
                    datetime.now(timezone.utc)
                ),
            },
        )

    # ---------------------------------------------
    # Successful audit
    # ---------------------------------------------

    write_audit_log(
        session_id=session_id,
        action=action_type,
        route="action",
        tool_name=action_type,
        approval_id=approval_id,
        reviewer=reviewer,
        status="approved",
        details={
            "comment": comment,
            "payload": payload,
            "action_result": action_result,
        },
    )

    return {
        "approval_id": approval_id,
        "status": "approved",
        "reviewer": reviewer,
        "comment": comment,
        "action_result": action_result,
    }

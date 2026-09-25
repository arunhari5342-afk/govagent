from src.graph.state import GovAgentState
from src.mcp_server.tools import (
    get_leave_balance,
)
from src.observability.tracing import (
    trace_span,
)
from src.services.approval_service import (
    create_approval,
)


def action_agent(
    state: GovAgentState,
) -> GovAgentState:

    user_input = state[
        "user_input"
    ]

    user_input_lower = (
        user_input
        .lower()
        .strip()
    )

    session_id = state.get(
        "session_id",
        "unknown-session",
    )

    # -----------------------------------------------------
    # Leave balance - read-only tool
    # -----------------------------------------------------

    leave_balance_request = (
        "leave balance"
        in user_input_lower
        or "remaining leave"
        in user_input_lower
        or "how many leaves"
        in user_input_lower
    )

    if leave_balance_request:

        with trace_span(
            "tool.get_leave_balance",
            {
                "tool": "get_leave_balance",
                "employee_id": "EMP001",
            },
        ):

            result = get_leave_balance(
                "EMP001"
            )

        return {
            **state,
            "tool_result": result,
            "response": str(result),
        }

    # -----------------------------------------------------
    # Helpdesk ticket - write action
    # -----------------------------------------------------

    ticket_request = (
        "create ticket"
        in user_input_lower
        or "create a ticket"
        in user_input_lower
        or "raise a ticket"
        in user_input_lower
        or "raise ticket"
        in user_input_lower
        or "open a ticket"
        in user_input_lower
        or "submit a ticket"
        in user_input_lower
        or "report an issue"
        in user_input_lower
        or "it support"
        in user_input_lower
        or "helpdesk ticket"
        in user_input_lower
    )

    if ticket_request:

        payload = {
            "employee_id": "EMP001",
            "title": "IT Helpdesk Request",
            "description": user_input,
        }

        approval = create_approval(
            session_id=session_id,
            action_type="create_ticket",
            payload=payload,
        )

        approval_id = approval[
            "id"
        ]

        approval_ui = {
            "type": "approval_request",
            "id": approval_id,
            "title": (
                "IT Helpdesk Ticket Approval"
            ),
            "message": (
                "A helpdesk ticket requires "
                "human approval before creation."
            ),
            "action": {
                "action_type": "create_ticket",
                "employee_id": "EMP001",
            },
            "actions": [
                {
                    "id": "approve",
                    "label": "Approve",
                    "method": "POST",
                    "path": (
                        f"/approvals/"
                        f"{approval_id}"
                    ),
                    "body": {
                        "approved": True,
                    },
                },
                {
                    "id": "reject",
                    "label": "Reject",
                    "method": "POST",
                    "path": (
                        f"/approvals/"
                        f"{approval_id}"
                    ),
                    "body": {
                        "approved": False,
                    },
                },
            ],
        }

        return {
            **state,
            "approval": approval_ui,
            "tool_result": {
                "approval_id": approval_id,
                "status": "pending",
            },
            "response": (
                "The helpdesk ticket is waiting "
                "for human approval."
            ),
        }

    # -----------------------------------------------------
    # Unknown action
    # -----------------------------------------------------

    return {
        **state,
        "response": (
            "I could not determine which "
            "authorized action should be performed."
        ),
    }
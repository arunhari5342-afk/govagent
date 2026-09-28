import re
from concurrent.futures import (
    ThreadPoolExecutor,
    TimeoutError,
)

from src.graph.state import GovAgentState
from src.mcp_server.tools import (
    create_ticket,
    get_leave_balance,
)
from src.observability.tracing import trace_span
from src.services.approval_service import (
    create_approval,
)
from src.governance.audit import write_audit_log


TOOL_TIMEOUT_SECONDS = 5


def run_tool_with_timeout(
    tool_function,
    *,
    timeout_seconds: int = TOOL_TIMEOUT_SECONDS,
    **kwargs,
):
    """Run a tool with a bounded execution time."""

    with ThreadPoolExecutor(
        max_workers=1
    ) as executor:

        future = executor.submit(
            tool_function,
            **kwargs,
        )

        return future.result(
            timeout=timeout_seconds
        )


def action_agent(
    state: GovAgentState,
) -> GovAgentState:

    user_input = state["user_input"]
    normalized = user_input.lower()

    session_id = state.get(
        "session_id",
        "default-session",
    )

    # ---------------------------------------------
    # Leave balance = READ action
    # ---------------------------------------------

    if (
        "leave balance" in normalized
        or "how much leave" in normalized
        or "remaining leave" in normalized
    ):

        try:
            with trace_span(
                "tool.get_leave_balance",
                {
                    "employee_id": "EMP001",
                    "timeout_seconds": (
                        TOOL_TIMEOUT_SECONDS
                    ),
                },
            ):

                result = run_tool_with_timeout(
                    get_leave_balance,
                    timeout_seconds=(
                        TOOL_TIMEOUT_SECONDS
                    ),
                    employee_id="EMP001",
                )

        except TimeoutError:

            write_audit_log(
                session_id=session_id,
                action="get_leave_balance",
                route="action",
                tool_name="get_leave_balance",
                status="timeout",
                details={
                    "timeout_seconds": (
                        TOOL_TIMEOUT_SECONDS
                    ),
                },
            )

            return {
                **state,
                "response": (
                    "The leave-balance service "
                    "timed out. No action was completed."
                ),
                "tool_result": {
                    "status": "timeout",
                },
            }

        except Exception as exc:

            write_audit_log(
                session_id=session_id,
                action="get_leave_balance",
                route="action",
                tool_name="get_leave_balance",
                status="error",
                details={
                    "error": str(exc),
                },
            )

            return {
                **state,
                "response": (
                    "The leave-balance service "
                    "could not be reached."
                ),
                "tool_result": {
                    "status": "error",
                },
            }

        write_audit_log(
            session_id=session_id,
            action="get_leave_balance",
            route="action",
            tool_name="get_leave_balance",
            status="success",
            details={
                "employee_id": "EMP001",
            },
        )

        return {
            **state,
            "tool_result": result,
            "response": str(result),
        }

    # ---------------------------------------------
    # create_ticket = WRITE action
    # ---------------------------------------------

    ticket_keywords = [
        "create ticket",
        "create an it ticket",
        "raise a ticket",
        "open a ticket",
        "helpdesk ticket",
    ]

    if any(
        keyword in normalized
        for keyword in ticket_keywords
    ):

        approval_id = create_approval(
            session_id=session_id,
            action_type="create_ticket",
            payload={
                "employee_id": "EMP001",
                "title": "IT Helpdesk Request",
                "description": user_input,
                "priority": "normal",
            },
        )

        return {
            **state,
            "approval": {
                "approval_id": approval_id,
                "status": "pending",
                "action": "create_ticket",
                "message": (
                    "Human approval is required "
                    "before creating this ticket."
                ),
            },
            "response": (
                "I prepared the IT helpdesk ticket. "
                "Human approval is required before "
                "the ticket can be created."
            ),
        }

    return {
        **state,
        "response": (
            "I could not determine the requested action."
        ),
    }
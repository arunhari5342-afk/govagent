from mcp.server.fastmcp import FastMCP

from .database import initialize_mock_data
from .tools import create_ticket
from .tools import get_leave_balance


mcp = FastMCP("GovAgent Enterprise Tools")


@mcp.tool()
def get_leave_balance_tool(employee_id: str) -> dict:
    """
    Get the current leave balance for an employee.
    """
    return get_leave_balance(employee_id)


@mcp.tool()
def create_ticket_tool(
    employee_id: str,
    title: str,
    description: str,
) -> dict:
    """
    Create an IT helpdesk ticket.
    """
    return create_ticket(
        employee_id=employee_id,
        title=title,
        description=description,
    )


if __name__ == "__main__":
    initialize_mock_data()

    mcp.run(transport="stdio")
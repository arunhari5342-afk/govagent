from mcp.server.fastmcp import FastMCP

from .database import initialize_mock_data
from .tools import create_ticket, get_leave_balance, search_policy

mcp = FastMCP("GovAgent Enterprise Tools")


@mcp.tool()
def get_leave_balance_tool(
    employee_id: str,
) -> dict:
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


@mcp.tool()
def search_policy_tool(
    query: str,
) -> dict:
    """
    Search enterprise policy documents.
    """

    return search_policy(query)


if __name__ == "__main__":
    initialize_mock_data()

    mcp.run(transport="stdio")

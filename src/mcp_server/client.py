import asyncio
import os
import sys
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _server_parameters() -> StdioServerParameters:
    python_executable = sys.executable

    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT)

    return StdioServerParameters(
        command=python_executable,
        args=[
            "-m",
            "src.mcp_server.server",
        ],
        env=env,
    )


async def _list_tools_async() -> list[dict[str, Any]]:
    server_params = _server_parameters()

    async with stdio_client(server_params) as (read, write), ClientSession(
        read, write
    ) as session:

        result = await session.list_tools()

        return [
            {
                "name": tool.name,
                "description": tool.description,
            }
            for tool in result.tools
        ]


async def _call_tool_async(
    tool_name: str,
    arguments: dict[str, Any],
) -> Any:

    server_params = _server_parameters()

    async with stdio_client(server_params) as (read, write), ClientSession(
        read, write
    ) as session:

        await session.initialize()

        result = await session.call_tool(
            tool_name,
            arguments,
        )

        if result.isError:
            raise RuntimeError(f"MCP tool '{tool_name}' returned an error.")

        structured_content = getattr(
            result,
            "structuredContent",
            None,
        )

        if structured_content is not None:
            return structured_content

        content = getattr(
            result,
            "content",
            [],
        )

        values = []

        for item in content:
            text_value = getattr(
                item,
                "text",
                None,
            )

            if text_value is not None:
                values.append(text_value)

        if len(values) == 1:
            return values[0]

        return values


def discover_tools() -> list[dict[str, Any]]:
    """
    Discover tools exposed by the GovAgent MCP server.
    """
    return asyncio.run(_list_tools_async())


def call_mcp_tool(
    tool_name: str,
    arguments: dict[str, Any],
) -> Any:
    """
    Invoke an MCP tool through the real MCP client/server connection.
    """
    return asyncio.run(
        _call_tool_async(
            tool_name,
            arguments,
        )
    )


def get_leave_balance(
    employee_id: str,
) -> Any:
    return call_mcp_tool(
        "get_leave_balance_tool",
        {
            "employee_id": employee_id,
        },
    )


def create_ticket(
    employee_id: str,
    title: str,
    description: str,
) -> Any:
    return call_mcp_tool(
        "create_ticket_tool",
        {
            "employee_id": employee_id,
            "title": title,
            "description": description,
        },
    )


def search_policy(
    query: str,
) -> Any:
    return call_mcp_tool(
        "search_policy_tool",
        {
            "query": query,
        },
    )

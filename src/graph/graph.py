from langgraph.graph import (
    END,
    START,
    StateGraph,
)

from src.governance.guard import (
    governance_guard,
)
from src.graph.action_agent import (
    action_agent,
)
from src.graph.policy_rag_agent import (
    policy_rag_agent,
)
from src.graph.reviewer_agent import (
    reviewer_agent,
)
from src.graph.router import (
    router_node,
)
from src.graph.state import (
    GovAgentState,
)


def route_after_guard(
    state: GovAgentState,
):
    status = state.get("governance_status")

    if status in {
        "blocked",
        "budget_exceeded",
    }:
        return "blocked"

    if state.get("route") == "action":
        return "action_agent"

    return "policy_rag_agent"


def build_graph():

    builder = StateGraph(GovAgentState)

    builder.add_node(
        "router",
        router_node,
    )

    builder.add_node(
        "governance_guard",
        governance_guard,
    )

    builder.add_node(
        "policy_rag_agent",
        policy_rag_agent,
    )

    builder.add_node(
        "reviewer_agent",
        reviewer_agent,
    )

    builder.add_node(
        "action_agent",
        action_agent,
    )

    builder.add_edge(
        START,
        "router",
    )

    builder.add_edge(
        "router",
        "governance_guard",
    )

    builder.add_conditional_edges(
        "governance_guard",
        route_after_guard,
        {
            "blocked": END,
            "policy_rag_agent": "policy_rag_agent",
            "action_agent": "action_agent",
        },
    )

    builder.add_edge(
        "policy_rag_agent",
        "reviewer_agent",
    )

    builder.add_edge(
        "reviewer_agent",
        END,
    )

    builder.add_edge(
        "action_agent",
        END,
    )

    return builder

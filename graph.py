from langgraph.graph import StateGraph, END
from backend.state import AgentState
from backend.agent.prompt_classification import classify_prompt
from backend.agent.router import router

from backend.lookup.lookup_agent import lookup_agent


def create_agent_graph():
    graph = StateGraph(AgentState)
    graph.set_entry_point("classify_prompt")

    graph.add_node("classify_prompt", classify_prompt)
    graph.add_node("router", router)
    graph.add_node("lookup_agent", lookup_agent)

    graph.add_edge("classify_prompt", "router")

    graph.add_conditional_edges(
        "router",
        lambda state: (
            "lookup_agent" if state.route_plan and state.route_plan[0] == "stock_lookup" else
            END
        )
    )

    return graph.compile()

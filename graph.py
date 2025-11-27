from langgraph.graph import StateGraph, END
from state import AgentState
from prompt_classification import classify_prompt
from router import router, lookup_agent
import httpx


def create_agent_graph():
    graph = StateGraph(AgentState)
    graph.set_entry_point("classify_prompt")

    graph.add_node("classify_prompt", classify_prompt)
    graph.add_node("router", router)
    graph.add_node("lookup_agent", lookup_agent)

    graph.add_edge("classify_prompt", "router")

    def route_switch(state: AgentState):
        plan = state.route_plan or []
        if not plan:
            return "END"
        head = plan[0]
        if head == "stock_lookup":
            return "lookup_agent"
        return "END"

    graph.add_conditional_edges(
        "router",
        route_switch,
        {
            "lookup_agent": "lookup_agent",
            "END": END,
        },
    )

    graph.add_edge("lookup_agent", END)

    return graph.compile()

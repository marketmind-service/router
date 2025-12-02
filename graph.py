from langgraph.graph import StateGraph, END
from state import AgentState
from prompt_classification import classify_prompt
from router import router, lookup_agent, news_agent, sector_agent


def create_agent_graph():
    graph = StateGraph(AgentState)
    graph.set_entry_point("classify_prompt")

    graph.add_node("classify_prompt", classify_prompt)
    graph.add_node("router", router)
    graph.add_node("lookup_agent", lookup_agent)
    graph.add_node("news_agent", news_agent)
    graph.add_node("sector_agent", sector_agent)

    graph.add_edge("classify_prompt", "router")

    def route_switch(state: AgentState):
        plan = state.route_plan or []
        if not plan:
            return "END"
        head = plan[0]
        if head == "stock_lookup":
            print("route_switch: stock_lookup")
            return "lookup_agent"
        if head == "news_sentiment":
            print("route_switch: news_sentiment")
            return "news_agent"
        if head == "sector_analysis":
            print("route_switch: sector_analysis")
            return "sector_agent"
        return "END"

    graph.add_conditional_edges(
        "router",
        route_switch,
        {
            "lookup_agent": "lookup_agent",
            "news_agent": "news_agent",
            "sector_agent": "sector_agent",
            "END": END,
        },
    )

    graph.add_edge("lookup_agent", END)
    graph.add_edge("news_agent", END)
    graph.add_edge("sector_agent", END)

    return graph.compile()

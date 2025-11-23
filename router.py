from state import AgentState


async def router(state: AgentState) -> AgentState:
    head = state.classification[0] if state.classification else None
    route = []

    if head == "Stock Lookup":
        route.append("stock_lookup")
    elif head == "SMA/EMA Analyzer":
        print("routing -> sma_ema")
    elif head == "Portfolio Simulator":
        print("routing -> portfolio_sim")
    elif head == "News & Sentiment":
        print("routing -> news_sentiment")
    elif head == "Sector Rotation Intelligence":
        print("routing -> sector_rotation")
    else:
        print("routing -> default")

    return state.model_copy(update={
        "route_plan": route,
        "route_taken": (state.route_taken or []) + ["router"],
    })

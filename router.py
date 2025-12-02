import os
import httpx
from state import AgentState


async def router(state: AgentState) -> AgentState:
    head = state.classification[0] if state.classification else None
    route = []

    if head == "Stock Lookup":
        route.append("stock_lookup")
    elif head == "SMA/EMA Analyzer":
        print("routing -> sma_ema")
    elif head == "Portfolio":
        print("routing -> portfolio")
    elif head == "News & Sentiment":
        route.append("news_sentiment")
    elif head == "Sector Analysis":
        route.append("sector_analysis")
    else:
        print("routing -> default")

    return state.model_copy(update={
        "route_plan": route,
        "route_taken": (state.route_taken or []) + ["router"],
    })


async def lookup_agent(state: AgentState) -> AgentState:
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.post(
            f"{os.environ.get("LOOKUP_BASE_URL")}/api/lookup-agent",
            json=state.model_dump(),
        )
        r.raise_for_status()
        data = r.json()

    # build a new AgentState from the response
    new_state = AgentState(**data)
    new_state.route_taken = (state.route_taken or []) + ["lookup_agent"]
    return new_state


async def news_agent(state: AgentState) -> AgentState:
    print("news_agent checkpoint 1")
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.post(
            f"{os.environ.get("NEWS_BASE_URL")}/api/news-agent",
            json=state.model_dump(),
        )
        print("news_agent checkpoint 2")
        r.raise_for_status()
        data = r.json()

    print("news_agent checkpoint 3")
    new_state = AgentState(**data)
    print(new_state)
    new_state.route_taken = (state.route_taken or []) + ["news_agent"]
    return new_state


async def sector_agent(state: AgentState) -> AgentState:
    print("sector_agent checkpoint 1")
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.post(
            f"{os.environ.get("SECTOR_BASE_URL")}/api/sector_agent",
            json=state.model_dump(),
        )
        print("sector_agent checkpoint 2")
        r.raise_for_status()
        data = r.json()

    print("sector_agent checkpoint 3")
    new_state = AgentState(**data)
    print(new_state)
    new_state.route_taken = (state.route_taken or []) + ["sector_agent"]
    return new_state

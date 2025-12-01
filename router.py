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
        print("routing -> news_sentiment")
    elif head == "Sector Rotation Intelligence":
        print("routing -> sector_rotation")
    else:
        print("routing -> default")

    return state.model_copy(update={
        "route_plan": route,
        "route_taken": (state.route_taken or []) + ["router"],
    })


LOOKUP_BASE_URL = os.environ.get(
    "LOOKUP_BASE_URL",
    "https://lookup.wonderfulfield-2268942f.eastus2.azurecontainerapps.io"
)


async def lookup_agent(state: AgentState) -> AgentState:
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.post(
            f"{LOOKUP_BASE_URL}/api/lookup-agent",
            json=state.model_dump(),
        )
        r.raise_for_status()
        data = r.json()

    # build a new AgentState from the response
    new_state = AgentState(**data)
    new_state.route_taken = (state.route_taken or []) + ["lookup_agent"]
    return new_state


NEWS_BASE_URL = os.environ.get(
    "NEWS_BASE_URL",
    "https://news-sentiment.wonderfulfield-2268942f.eastus2.azurecontainerapps.io"
)


async def news_agent(state: AgentState) -> AgentState:
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.post(
            f"{NEWS_BASE_URL}/api/news-agent",
            json=state.model_dump(),
        )
        r.raise_for_status()
        data = r.json()

    new_state = AgentState(**data)
    new_state.route_taken = (state.route_taken or []) + ["news_agent"]
    return new_state

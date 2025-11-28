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


LOOKUP_BASE_URL = os.environ.get(
    "LOOKUP_BASE_URL",
    "https://lookup.wonderfulfield-2268942f.eastus2.azurecontainerapps.io"
)


async def lookup_agent(state: AgentState) -> AgentState:
    prompt = state.prompt

    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(
            f"{LOOKUP_BASE_URL}/api/stock",
            params={
                "query": prompt,
                "period": "6mo",
                "interval": "1d",
            },
        )
        r.raise_for_status()
        data = r.json()

    return state.model_copy(update={
        "result": data,
        "route_taken": (state.route_taken or []) + ["lookup_agent"],
    })

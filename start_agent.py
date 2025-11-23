from typing import cast
from langchain_core.runnables import RunnableConfig
from state import AgentState
from graph import create_agent_graph


async def start_agent(prompt: str) -> AgentState:
    state = AgentState(prompt=prompt)
    result = await create_agent_graph().ainvoke(
        state,
        config=cast(RunnableConfig, cast(object, {"recursion_limit": 200}))
    )

    return AgentState(**result)

import textwrap

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from state import AgentState
from start_agent import start_agent

app = FastAPI(title="MarketMind Agent API")


class AskRequest(BaseModel):
    prompt: str


@app.get("/")
async def root():
    return {"status": "ok", "message": "MarketMind agent is alive"}


@app.post("/api/ask")
async def ask(req: AskRequest):
    prompt = (req.prompt or "").strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="prompt is required")

    try:
        result_state: AgentState = await start_agent(prompt)
    except Exception as e:
        # You can log e here if you have logging wired
        raise HTTPException(status_code=500, detail=f"agent_error: {e}")

    # Assuming AgentState is a Pydantic model (it looks like it from model_copy usage)
    if hasattr(result_state, "model_dump"):
        return result_state.model_dump()

    # Fallback in case AgentState is a dataclass or plain object
    if isinstance(result_state, AgentState):
        return result_state.__dict__

    # Last resort
    return {"result": str(result_state)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
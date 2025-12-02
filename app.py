#!/usr/bin/env python3
# app.py

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
    """
    Simple test route that runs a hardcoded prompt through the agent
    and shows the final AgentState on the page.
    """
    test_prompt = "Test prompt: briefly confirm the MarketMind agent is wired up."

    try:
        result_state: AgentState = await start_agent(test_prompt)
    except Exception as e:
        # This tells you if LangGraph / Azure / whatever is borked
        raise HTTPException(status_code=500, detail=f"agent_error: {e}")

    # Prefer Pydantic model_dump if AgentState is BaseModel
    if hasattr(result_state, "model_dump"):
        payload = result_state.model_dump()
    else:
        # Fallback if it's some other type
        payload = result_state.__dict__ if isinstance(result_state, AgentState) else str(result_state)

    # This is what shows in the browser at http://localhost:8000/
    return {
        "status": "ok",
        "test_prompt": test_prompt,
        "agent_state": payload,
    }


@app.post("/api/ask")
async def ask(req: AskRequest):
    prompt = (req.prompt or "").strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="prompt is required")

    try:
        result_state: AgentState = await start_agent(prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"agent_error: {e}")

    if hasattr(result_state, "model_dump"):
        return result_state.model_dump()

    if isinstance(result_state, AgentState):
        return result_state.__dict__

    return {"result": str(result_state)}

# === CLI MODE ===
async def local_cli():
    print("MarketMind CLI (type 'exit' to quit)")
    while True:
        prompt = input("\nYou: ").strip()
        if not prompt or prompt.lower() in {"exit", "quit"}:
            print("Done.")
            break
        try:
            result = await start_agent(prompt)
            print(textwrap.dedent(f"""
                ========================================== RESULTS ==========================================
                Prompt: {result.prompt}
                Classification: {result.classification}
                Company: {result.lookup_result.company or "None"}
                Ticker: {result.lookup_result.symbol or "None"}
                Period: {result.lookup_result.period or "None"}
                Interval: {result.lookup_result.interval or "None"}
                ------------------------------------------------
                Search: {result.lookup_result or "None"}
                News: {result.news_result or "None"}
                ------------------------------------------------
                SECTOR ANALYSIS
                Rows: {result.sector_result.raw_rows}
                Structured: {result.sector_result.structured_view}
                Commentary: {result.sector_result.interpreted_results}
                =============================================================================================
            """).strip())
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    # mode = input("Run [s]erver or [t]erminal? (s/t): ").strip().lower()
    mode = "t"
    if mode == "s":
        import uvicorn
        uvicorn.run("app:app", host="127.0.0.1", port=8080, reload=True)
    else:
        import asyncio
        asyncio.run(local_cli())


'''if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )'''
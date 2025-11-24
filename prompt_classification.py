import asyncio, textwrap, ast
from typing import List
from config import query
from state import AgentState
from langchain_core.messages import SystemMessage, HumanMessage


async def classify(prompt: str) -> List[str]:
    messages = [
        SystemMessage(content=textwrap.dedent("""
            Classify the user's finance question into exactly one category.

            Valid:
            ["Stock Lookup"]
            ["SMA/EMA Analyzer"]
            ["Portfolio Simulator"]
            ["News & Sentiment"]
            ["Sector Rotation Intelligence"]
            ["None of the above"]
            
            Rules:
            1. If it's about simulations or portfolio behavior → Portfolio Simulator
            2. If it's about a specific stock or ticker → Stock Lookup
            3. If it's about moving averages → SMA/EMA Analyzer
            4. If it's about headlines or sentiment → News & Sentiment
            5. If it's about sectors or industries → Sector Rotation Intelligence
            6. Otherwise → None of the above
            
            Respond ONLY with the JSON array.
        """).strip()),
        HumanMessage(content=f"Prompt: {prompt}")
    ]

    for attempt in range(3):
        response = query.invoke(messages)
        content = response.content if isinstance(response.content, str) else str(response.content)
        print(f"classify_prompt attempt {attempt + 1}: {content.strip()}")
        try:
            parsed = ast.literal_eval(content.strip())
        except Exception:
            parsed = None
        if isinstance(parsed, list) and all(isinstance(x, str) for x in parsed):
            return parsed
        if attempt < 2:
            wait = 0.5 * (2 ** attempt)
            print(f"Invalid parse, retrying after {wait} seconds...")
            await asyncio.sleep(wait)
    print("classify_prompt: exhausted retries, returning []")
    return []


async def classify_prompt(state: AgentState) -> AgentState:
    print("classify_prompt")
    classification = await classify(state.prompt)

    return state.model_copy(update={
        "classification": classification,
        "route_taken": (state.route_taken or []) + ["prompt_classification"],
    })

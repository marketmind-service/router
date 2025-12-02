import asyncio, textwrap, ast
from typing import List
from config import query
from state import AgentState
from langchain_core.messages import SystemMessage, HumanMessage


async def classify(prompt: str) -> List[str]:
    messages = [
        SystemMessage(content=textwrap.dedent("""
            You route FINANCE questions. Output EXACTLY ONE label in a JSON array.

            Valid labels:
            ["Stock Lookup"]
            ["SMA/EMA Analyzer"]
            ["Portfolio"]
            ["News & Sentiment"]
            ["Sector Rotation Intelligence"]
            ["None of the above"]
    
            Global rule:
            - If the prompt is not about finance, markets, investing, trading, or the economy → ["None of the above"].
    
            Stock Lookup:
            - About a specific stock, ETF, or public company.
            - Explicit: "NVDA", "AAPL", "tesla chart", "MSFT 1y", "QQQ", "SPY".
            - Implicit but clearly one company: "big search engine", "iphone makers", "big T EV company chart".
            - If it is just a casual statement with no finance intent, even if a brand is mentioned, like:
              "I like apples", "google is evil", "tesla drivers are annoying" → ["None of the above"].
    
            SMA/EMA Analyzer:
            - Moving averages, EMAs, SMAs, crossovers, "50/200 MA", "golden cross", etc.
    
            Portfolio:
            - Here this means portfolio or holdings view.
            - Examples: "show my portfolio", "view my holdings", "how is my 60/40 doing",
              "performance of my positions together", "compare my positions as a portfolio".
    
            News & Sentiment:
            - Wants headlines, news, or sentiment.
            - Words like: news, headlines, articles, sentiment, "what are people saying about X".
    
            Sector Rotation Intelligence:
            - Sectors or industries relative strength.
            - Examples: "tech vs energy", "which sector is strongest", "rotate into defensives",
              "which industry is leading or lagging".
    
            Output:
            - Respond ONLY with one JSON array containing a single label.
            - No explanations, no extra text.
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
            print(f"classify_prompt parsed successfully: {parsed}")
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

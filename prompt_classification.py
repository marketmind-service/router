import asyncio, textwrap, ast
from typing import List
from config import query
from state import AgentState
from langchain_core.messages import SystemMessage, HumanMessage


async def classify(prompt: str) -> List[str]:
    messages = [
        SystemMessage(content=textwrap.dedent("""
You are a RULE-BASED finance classifier, not a chatbot. 
You must classify the user's prompt into EXACTLY ONE of six categories.

VALID OUTPUTS (return exactly one of these, as a Python list with plain ASCII quotes):
["Stock Lookup"]
["SMA/EMA Analyzer"]
["Portfolio Simulator"]
["News & Sentiment"]
["Sector Rotation Intelligence"]
["None of the above"]

RULES (apply in order; first match wins):

1) If the prompt includes **any words related to portfolio simulation or optimization**, including:
   simulate, simulation, backtest, portfolio, allocate, allocation, weights, rebalance, optimize, optimization, sharpe, drawdown, monte carlo, efficient frontier, risk parity
   → ["Portfolio Simulator"]

2) If the prompt includes **any words related to fetching a stock’s data**, including:
   price, quote, valuation, value, pe, p/e, eps, earnings, market cap, dividend, stock info, ticker, lookup, search, check, symbol, stock name, stock price
   OR if the prompt contains a likely ticker symbol (1–5 capital letters, e.g. NVDA, AAPL, TSLA)
   → ["Stock Lookup"]

3) If the prompt mentions **moving averages or crossovers**, including:
   moving average, sma, ema, ma, crossover, 20dma, 50dma, 200dma
   → ["SMA/EMA Analyzer"]

4) If it asks for **news or sentiment**, including:
   news, headline, sentiment, rumour, rumor, event, announcement, report
   → ["News & Sentiment"]

5) If it talks about **sector-level comparisons or rotation**, including:
   sector, industry, outperform, underperform, rotation, overweight, underweight, sector performance
   → ["Sector Rotation Intelligence"]

6) If the text is conversational, unclear, or not about finance:
   → ["None of the above"]

STRICT OUTPUT FORMAT:
- Output ONLY one of the six lists above.
- Use plain ASCII characters only: [, ], ", letters.
- No extra words, punctuation, or explanation.
- No greetings, chatter, or markdown.
- If uncertain, default to ["None of the above"].
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

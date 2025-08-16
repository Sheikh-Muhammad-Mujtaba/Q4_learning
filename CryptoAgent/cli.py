    from agents import Runner, Agent, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
from dotenv import load_dotenv
import os, asyncio, requests

# Load environment
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found!")

MODEL = "gemini-2.0-flash" #"meta-llama/llama-4-scout:free"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/" #"https://openrouter.ai/api/v1"
client = AsyncOpenAI(api_key=api_key, base_url=BASE_URL)
set_tracing_disabled(disabled=True)

# Tool: Get price of a specific coin
@function_tool
async def get_crypto_price(name: str = "bitcoin") -> dict:
    try:
        print(f"Fetching price for coin: {name}")
        response = requests.get(
            "https://api.coinlore.net/api/tickers/",
            headers={"User-Agent": "CryptoAgent/1.0"},
            timeout=10
        )
        response.raise_for_status()
        coins = response.json().get("data", [])
    except Exception as e:
        return {"error": f"Failed to fetch data: {e}"}

    for coin in coins:
        if name.lower() in [coin["name"].lower(), coin["symbol"].lower(), coin["nameid"].lower()]:
            return {
                "name": coin["name"],
                "symbol": coin["symbol"],
                "price_usd": coin["price_usd"],
                "change_24h": coin["percent_change_24h"],
                "market_cap": coin["market_cap_usd"]
            }

    return {"error": f"Coin '{name}' not found. Try using the Coin ID instead."}

# Tool: Get top trending coins
@function_tool
async def get_crypto_info(start: int = 0, limit: int = 100) -> dict:
    try:
        print(f"Fetching crypto data from start={start} to limit={limit}")
        response = requests.get(
            f"https://api.coinlore.net/api/tickers/?start={start}&limit={limit}",
            headers={"User-Agent": "CryptoAgent/1.0"},
            timeout=10
        )
        response.raise_for_status()
        coins = response.json().get("data", [])
    except Exception as e:
        return {"error": f"Failed to fetch data: {e}"}

    trending = sorted(coins, key=lambda c: abs(float(c["percent_change_24h"])), reverse=True)[:5]
    return {
        "trending": [
            {
                "name": coin["name"],
                "symbol": coin["symbol"],
                "price_usd": coin["price_usd"],
                "change_24h": coin["percent_change_24h"]
            }
            for coin in trending
        ]
    }

# Agent definition
agent = Agent(
    name="CryptoDataAgent",
    instructions="""
You are a crypto assistant. You have two tools:
- Use `get_crypto_price(name)` when the user asks for a specific coin's price.
- Use `get_crypto_info(start, limit)` when the user asks for trending coins or top movers.

ALWAYS use the tool output to answer directly.
Format trending coins as:
- Coin Name (Symbol): $Price — 24h Δ: %

Keep responses to 2–3 lines max. Never just say "no action needed". If coin is not found, tell user and suggest using Coin ID.
""",
    model=OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
    tools=[get_crypto_info, get_crypto_price]
)

# Runner
async def main():
    try:
        result = await Runner.run(agent, "What is price of eth and btc?")
        print(result.final_output)
    except Exception as e:
        print("🔐 Authentication failed:", e)
        print("Try switching to a different model or recheck your API key.")

if __name__ == "__main__":
    asyncio.run(main())

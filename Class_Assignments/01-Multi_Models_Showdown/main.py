import asyncio
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
import os
import dotenv
import streamlit as st

dotenv.load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "deepseek/deepseek-chat-v3-0324:free"
MODEL2 = "google/gemini-2.0-flash-exp:free"
MODEL3 = "mistralai/devstral-small:free"
MODEL4 = "microsoft/mai-ds-r1:free"
MODEL5 = "qwen/qwen3-235b-a22b:free"

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)


set_tracing_disabled(disabled=True)

async def main():
    # This agent will use the custom LLM provider
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model=OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
    )

    result = await Runner.run(
        agent,
        "Tell me about recursion in programming.",
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
     
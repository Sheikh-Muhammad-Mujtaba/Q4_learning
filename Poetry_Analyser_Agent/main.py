from agents import Runner, Agent, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, handoff, RunContextWrapper
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from dotenv import load_dotenv
import os, asyncio
from pydantic import BaseModel

# Load environment
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found!")

MODEL = "gemini-2.0-flash" 
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/" 
client = AsyncOpenAI(api_key=api_key, base_url=BASE_URL)
# set_tracing_disabled(disabled=True)

class EscalationData(BaseModel):
    reason: str
    
handoff_reason = None
def on_handoff(ctx: RunContextWrapper[None], input_data: EscalationData):
    global handoff_reason
    handoff_reason = input_data.reason
    
    
    
def get_agent_name(new_items: list) -> tuple:
    handoff_target_agent = None

    for item in new_items:
        if getattr(item, 'type', '') == 'handoff_output_item':
            handoff_target_agent = getattr(item.target_agent, 'name', None)
        
    return handoff_target_agent 

lyric_agent = Agent(
    name="Lyric Agent",
    instructions="""
    {RECOMMENDED_PROMPT_PREFIX}
    you are a Lyric poetry expert agent. you will answer questions about lyric poetry.
    Lyric poetry is when poets write about their own feelings and thoughts, like songs or poems about being sad or happy.
    your tasks are to answer in a way that is easy to understand, if user only provide you poem or stanza, you will analyse it and provide a summary of the poem.
    """,
    model=OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
    )

narrative_agent = Agent(
    name="Narrative Agent",
    instructions="""
    {RECOMMENDED_PROMPT_PREFIX}
    you are a Narrative poetry expert agent. you will answer questions about narrative poetry.
    Narrative poetry tells a story with characters and events, just like a regular story but written in poem form with rhymes or special rhythm.
    your tasks are to answer in a way that is easy to understand, if user only provide you poem or stanza, you will analyse it and provide a summary of the poem.
    """,
    model=OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
)

dramatic_agent = Agent(
    name="Dramatic Agent",
    instructions="""
    {RECOMMENDED_PROMPT_PREFIX}
    you are a Dramatic poetry expert agent. you will answer questions about dramatic poetry.
    Dramatic poetry is meant to be performed out loud, where someone acts like a character and speaks their thoughts and feelings to an audience (acting in a theatre).
    your tasks are to answer in a way that is easy to understand, if user only provide you poem or stanza, you will analyse it and provide a summary of the poem.
    """,
    model=OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
)

# Agent definition
agent = Agent(
    name="Poetry Analyser",
    instructions="""
    you are a Poetry Analyser agent. you will analyze poetry type and handoff to the appropriate agent by calling the correct tool.
    Always include a clear reason in the 'reason' field of the handoff arguments, explaining *why* the poem matches the type.

    If it's lyric poetry, call `transfer_to_lyric_agent` with a reason.
    If it's narrative poetry, call `transfer_to_narrative_agent` with a reason.
    If it's dramatic poetry, call `transfer_to_dramatic_agent` with a reason.
    If it's other types of poetry, answer directly in an easy-to-understand way.

    When handing off, provide the poem or stanza, and set the 'reason' field accordingly.
    """,
    model=OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
    handoffs=[ 
              handoff(
                  agent=lyric_agent,
                  on_handoff=on_handoff,
                  input_type=EscalationData,
                  ), 
              handoff(
                  agent=narrative_agent,
                  on_handoff=on_handoff,
                  input_type=EscalationData,
                  ), 
              handoff(
                  agent=dramatic_agent,
                  on_handoff=on_handoff,
                  input_type=EscalationData,
                  ) 
              ]
)


# Runner
async def main():
    try:
        result = await Runner.run(agent, "Friends, Romans, countrymen, lend me your ears; I come to bury Caesar, not to praise him.")
        handoff_target_agent = get_agent_name(result.new_items)
        print("=" * 30)
        print(f"Handoff to {handoff_target_agent}")
        print(f"Agent called with reason: \n\t\t{handoff_reason}")
        print("=" * 30)
        print(result.final_output)
    except Exception as e:
        print("run into error", e)

if __name__ == "__main__":
    asyncio.run(main())

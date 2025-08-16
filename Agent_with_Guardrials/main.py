from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, handoff, RunContextWrapper, TResponseInputItem, GuardrailFunctionOutput, input_guardrail, output_guardrail
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from dotenv import load_dotenv
import os
import asyncio
from pydantic import BaseModel

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")


MODEL = "gemini-2.0-flash"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
client = AsyncOpenAI(api_key=api_key, base_url=BASE_URL)
model = OpenAIChatCompletionsModel(model=MODEL, openai_client=client)

class OnTopic(BaseModel):
    reasoning: str
    NotTeacherTask: bool
    CanNotHandledByAdmin: bool

class OutputInfo(BaseModel):
    reasoning: str
    NotWellExplained: bool
    
Input_guardrail_agent = Agent(
    name="Guardrail check",
    instructions=f"""
     You are Guardrail agent you have to Check if the user is asking you to do their math homework, or something which is not teacher responsiblity.
    example: "can you do my homework" is not related to teaching.
    so the teacher_agent should not answer this question, do not triggred if task can be handoffed to the admin agent.
    """,
    output_type=OnTopic,
    model=model
)

output_guardrail_agent = Input_guardrail_agent.clone(
    name="Output Guardrail check",
    instructions=f"""
    You are Guardrail agent you have to Check if you your responce is not well explained, you should verify it to be well explaind.
    """,
    output_type=OutputInfo,
)

@input_guardrail
async def admin_guardrail(ctx: RunContextWrapper[OnTopic],  agent: Agent, input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
    result = await Runner.run(
        Input_guardrail_agent,
        input,
        context=ctx.context,
    )
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.NotTeacherTask and result.final_output.CanNotHandledByAdmin
    )

@output_guardrail
async def output_guardrail(ctx: RunContextWrapper[OutputInfo], agent: Agent, input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
    result = await Runner.run(
        output_guardrail_agent,
        input,
        context=ctx.context,
    )
    
    return GuardrailFunctionOutput(
            output_info=result.final_output,
            tripwire_triggered=result.final_output.NotWellExplained
        )


admin_agent = Agent(
    name="Admin Agent",
    instructions=f"""
    {RECOMMENDED_PROMPT_PREFIX}
    You are an Admin Agent, your tasks are to handle administrative tasks like changing class timings,
    You should not answer questions related to teaching or learning materials.
    and if something not your responsibility, you have to just say it's not my task.
    """,
    model=model,
    output_guardrails=[output_guardrail],
)

teacher_agent = Agent(
    name="Teaching Agent",
    instructions=f"""
    {RECOMMENDED_PROMPT_PREFIX}
    You are a Teaching Assistant helping students learn about AI and machine learning.
    Your tasks are to answer questions, provide explanations, and assist with learning materials.
    if the user asks you to do their math homework, or something which is not teacher responsiblity, like administrative tasks,
    you should handoff to the Admin Agent.
    """,
    model=model,
    handoffs=[admin_agent],
    input_guardrails=[admin_guardrail],
)



# Runner
async def main():
    try:
        result = await Runner.run(teacher_agent, "I want to verify my fees status")
        print(result.final_output)
    except Exception as e:
        print("run into error", e)

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import streamlit as st
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
import os
import dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
dotenv.load_dotenv()

# Streamlit page configuration
st.set_page_config(
    page_title="Multi Model Showdown",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="auto",
)

# Configuration
API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"
MODELS = {
    "DeepSeek": "deepseek/deepseek-chat-v3-0324:free",
    "Gemini": "google/gemini-2.0-flash-exp:free",
    "Mistral": "mistralai/devstral-small:free",
    "Microsoft": "microsoft/mai-ds-r1:free",
    "Qwen": "qwen/qwen3-235b-a22b:free"
}

# Initialize client
client = AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL)
set_tracing_disabled(disabled=True)

# Custom CSS for styling
with open("style.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

async def get_model_response(model_name: str, model_id: str, prompt: str):
    """Get response from a single model with error handling"""
    try:
        agent = Agent(
            name=model_name,
            instructions="You are a helpful AI assistant. Provide concise and accurate responses in simple and easy english.",
            model=OpenAIChatCompletionsModel(
                model=model_id, openai_client=client),
        )

        result = await Runner.run(agent, prompt)
        return {"success": True, "response": result.final_output, "error": None}

    except Exception as e:
        logger.error(f"Error with {model_name} ({model_id}): {str(e)}")
        return {"success": False, "response": None, "error": str(e)}


async def get_selected_responses(prompt: str, selected_models: list):
    """Get responses from selected models concurrently"""
    tasks = []
    for model_name in selected_models:
        model_id = MODELS[model_name]
        tasks.append(get_model_response(model_name, model_id, prompt))

    return await asyncio.gather(*tasks)


def display_response(model_name: str, response_data: dict):
    """Display response or error in a styled card"""
    card_class = "model-card" if response_data["success"] else "model-card error-card"
    content = response_data["response"] if response_data[
        "success"] else f"Error: {response_data['error']}"
    content_class = "response-text" if response_data["success"] else "error-text"

    st.markdown(f"""
    <div class="{card_class}">
        <div class="model-name">{model_name}</div>
        <div class="{content_class}">{content}</div>
    </div>
    """, unsafe_allow_html=True)


def main():
    st.title("🤖 Multi Model Showdown")
    st.markdown("Compare responses from different AI models side-by-side")

    # Sidebar with model selection
    with st.sidebar:
        st.header("Model Selection")
        st.write("Select the models you want to query:")
        selected_models = []
        for model_name in MODELS.keys():
            if st.checkbox(model_name, value=True, key=f"model_{model_name}"):
                selected_models.append(model_name)

        if not selected_models:
            st.warning("Please select at least one model")
            st.stop()

        st.markdown("---")

        if st.text_input("Enter your OpenRouter API Key:", type="password", key="api_key"):
            api_key = st.session_state.get("api_key")
            if api_key:
                client.api_key = api_key
                st.success("API Key updated successfully!")
            else:
                st.error("Please enter a valid API Key.")

    # Main content area
    prompt = st.text_area(
        "Enter your prompt:",
        "Explain quantum computing in simple terms",
        height=150
    )

    if st.button("Generate Responses", type="primary"):
        if not prompt.strip():
            st.warning("Please enter a prompt")
            st.stop()

        with st.spinner(f"Querying {len(selected_models)} models..."):
            try:
                all_responses = asyncio.run(
                    get_selected_responses(prompt, selected_models))

                st.subheader("Model Responses")
                cols = st.columns(2)

                successful_count = sum(
                    1 for r in all_responses if r["success"])

                for i, (model_name, response_data) in enumerate(zip(selected_models, all_responses)):
                    with cols[i % 2]:
                        display_response(model_name, response_data)

                st.markdown(f"""
                            <div style="color: #27ae60; font-weight: bold;">
                                ✅ Completed with {successful_count}/{len(selected_models)} successful responses
                            </div>
                            """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()

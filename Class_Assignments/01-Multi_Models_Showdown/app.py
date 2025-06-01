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
st.markdown("""
<style>
   /* Import futuristic fonts */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');

/* Global dark theme with cyber background */
.stApp {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
    color: #00ffff;
    font-family: 'Rajdhani', sans-serif;
}

/* Animated background grid */
.stApp::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        linear-gradient(rgba(0, 255, 255, 0.1) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 255, 255, 0.1) 1px, transparent 1px);
    background-size: 50px 50px;
    animation: gridMove 20s linear infinite;
    pointer-events: none;
    z-index: -1;
}

@keyframes gridMove {
    0% { transform: translate(0, 0); }
    100% { transform: translate(50px, 50px); }
}

/* Main title styling */
h1 {
    font-family: 'Orbitron', monospace !important;
    font-weight: 900 !important;
    color: #00ffff !important;
    text-align: center !important;
    font-size: 3rem !important;
    text-shadow: 
        0 0 10px #00ffff,
        0 0 20px #00ffff,
        0 0 30px #00ffff,
        0 0 40px #00ffff;
    border: none !important;
    padding: 2rem 0 !important;
    margin-bottom: 2rem !important;
    animation: titleGlow 2s ease-in-out infinite alternate;
}

@keyframes titleGlow {
    from { text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff, 0 0 30px #00ffff; }
    to { text-shadow: 0 0 20px #00ffff, 0 0 30px #00ffff, 0 0 40px #00ffff, 0 0 50px #00ffff; }
}

/* Subtitle styling */
.stApp > div > div > div > div > div:nth-child(2) {
    text-align: center;
    color: #ff00ff;
    font-size: 1.2rem;
    margin-bottom: 2rem;
    text-shadow: 0 0 10px #ff00ff;
}

/* Sidebar styling */
.css-1d391kg {
    background: linear-gradient(180deg, #0f0f23 0%, #1a1a2e 100%) !important;
    border-right: 2px solid #00ffff !important;
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.3) !important;
}

/* Sidebar headers */
.css-1d391kg h2 {
    color: #00ffff !important;
    font-family: 'Orbitron', monospace !important;
    text-shadow: 0 0 10px #00ffff !important;
    border-bottom: 1px solid #00ffff !important;
    padding-bottom: 0.5rem !important;
}

/* Model cards - cyber style */
.model-card {
    background: linear-gradient(145deg, #1a1a2e, #16213e) !important;
    border: 2px solid #00ffff !important;
    border-radius: 15px !important;
    padding: 1.5rem !important;
    margin-bottom: 1.5rem !important;
    box-shadow: 
        0 0 20px rgba(0, 255, 255, 0.3),
        inset 0 0 20px rgba(0, 255, 255, 0.1) !important;
    transition: all 0.3s ease !important;
    position: relative !important;
    overflow: hidden !important;
}

.model-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.2), transparent);
    transition: left 0.5s;
}

.model-card:hover::before {
    left: 100%;
}

.model-card:hover {
    transform: translateY(-5px) scale(1.02) !important;
    border-color: #ff00ff !important;
    box-shadow: 
        0 10px 30px rgba(255, 0, 255, 0.4),
        inset 0 0 30px rgba(255, 0, 255, 0.1) !important;
}

/* Error cards */
.error-card {
    border-color: #ff0040 !important;
    background: linear-gradient(145deg, #2e1a1a, #3e1616) !important;
    box-shadow: 
        0 0 20px rgba(255, 0, 64, 0.3),
        inset 0 0 20px rgba(255, 0, 64, 0.1) !important;
}

/* Model names */
.model-name {
    font-family: 'Orbitron', monospace !important;
    font-weight: 700 !important;
    color: #00ffff !important;
    font-size: 1.3rem !important;
    text-shadow: 0 0 10px #00ffff !important;
    margin-bottom: 1rem !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
}

/* Response text */
.response-text {
    color: #e0e0e0 !important;
    line-height: 1.8 !important;
    font-size: 1rem !important;
    text-shadow: 0 0 5px rgba(224, 224, 224, 0.3) !important;
}

/* Error text */
.error-text {
    color: #ff4081 !important;
    font-style: italic !important;
    text-shadow: 0 0 10px #ff4081 !important;
}

/* Buttons - cyber style */
.stButton > button {
    background: linear-gradient(45deg, #00ffff, #ff00ff) !important;
    color: #000 !important;
    font-family: 'Orbitron', monospace !important;
    font-weight: bold !important;
    padding: 0.75rem 2rem !important;
    border: none !important;
    border-radius: 25px !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    box-shadow: 
        0 0 20px rgba(0, 255, 255, 0.5),
        inset 0 0 20px rgba(255, 255, 255, 0.1) !important;
    transition: all 0.3s ease !important;
    position: relative !important;
    overflow: hidden !important;
}

.stButton > button:hover {
    background: linear-gradient(45deg, #ff00ff, #00ffff) !important;
    transform: translateY(-2px) !important;
    box-shadow: 
        0 5px 25px rgba(255, 0, 255, 0.6),
        inset 0 0 30px rgba(255, 255, 255, 0.2) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* Text input styling */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(26, 26, 46, 0.8) !important;
    border: 2px solid #00ffff !important;
    border-radius: 10px !important;
    color: #00ffff !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important;
    padding: 1rem !important;
    box-shadow: inset 0 0 10px rgba(0, 255, 255, 0.2) !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #ff00ff !important;
    box-shadow: 
        inset 0 0 10px rgba(255, 0, 255, 0.2),
        0 0 20px rgba(255, 0, 255, 0.3) !important;
}

/* Checkboxes */
.stCheckbox > label {
    color: #00ffff !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 500 !important;
    font-size: 1.1rem !important;
}

.stCheckbox > label > div {
    border: 2px solid #00ffff !important;
    border-radius: 5px !important;
    background: rgba(26, 26, 46, 0.8) !important;
}

.stCheckbox > label > div[data-checked="true"] {
    background: linear-gradient(45deg, #00ffff, #ff00ff) !important;
    border-color: #ff00ff !important;
}

/* Spinner styling */
.stSpinner > div {
    border-top-color: #00ffff !important;
    border-right-color: #ff00ff !important;
}

/* Success/warning messages */
.stSuccess {
    background: linear-gradient(90deg, rgba(0, 255, 0, 0.1), rgba(0, 255, 255, 0.1)) !important;
    border: 1px solid #00ff00 !important;
    border-radius: 10px !important;
    color: #00ff00 !important;
    box-shadow: 0 0 15px rgba(0, 255, 0, 0.3) !important;
}

.stWarning {
    background: linear-gradient(90deg, rgba(255, 165, 0, 0.1), rgba(255, 255, 0, 0.1)) !important;
    border: 1px solid #ffaa00 !important;
    border-radius: 10px !important;
    color: #ffaa00 !important;
    box-shadow: 0 0 15px rgba(255, 170, 0, 0.3) !important;
}

.stError {
    background: linear-gradient(90deg, rgba(255, 0, 0, 0.1), rgba(255, 0, 100, 0.1)) !important;
    border: 1px solid #ff0040 !important;
    border-radius: 10px !important;
    color: #ff0040 !important;
    box-shadow: 0 0 15px rgba(255, 0, 64, 0.3) !important;
}

/* Success count styling */
.success-count {
    font-family: 'Orbitron', monospace !important;
    font-weight: bold !important;
    color: #00ff00 !important;
    text-shadow: 0 0 10px #00ff00 !important;
    font-size: 1.2rem !important;
}

/* Columns styling */
.css-ocqkz7 {
    gap: 2rem !important;
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 12px;
}

::-webkit-scrollbar-track {
    background: #1a1a2e;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #00ffff, #ff00ff);
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #ff00ff, #00ffff);
}

/* Loading animation */
@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
}

.stSpinner {
    animation: pulse 1.5s ease-in-out infinite;
}

/* Responsive design */
@media (max-width: 768px) {
    h1 {
        font-size: 2rem !important;
    }
    
    .model-card {
        margin-bottom: 1rem !important;
        padding: 1rem !important;
    }
    
    .model-name {
        font-size: 1.1rem !important;
    }
}

/* Additional cyber elements */
.cyber-border {
    position: relative;
}

.cyber-border::before {
    content: '';
    position: absolute;
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    background: linear-gradient(45deg, #00ffff, #ff00ff, #00ffff);
    border-radius: inherit;
    z-index: -1;
    animation: borderRotate 3s linear infinite;
}

@keyframes borderRotate {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Glitch effect for errors */
.error-card {
    animation: glitch 0.3s ease-in-out infinite alternate;
}

@keyframes glitch {
    0% { transform: translate(0); }
    20% { transform: translate(-2px, 2px); }
    40% { transform: translate(-2px, -2px); }
    60% { transform: translate(2px, 2px); }
    80% { transform: translate(2px, -2px); }
    100% { transform: translate(0); }
}
</style>
""", unsafe_allow_html=True)


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

        if st.button("Select All", type="primary"):
            selected_models = list(MODELS.keys())
            for model_name in MODELS.keys():
                st.session_state[f"model_{model_name}"] = True

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

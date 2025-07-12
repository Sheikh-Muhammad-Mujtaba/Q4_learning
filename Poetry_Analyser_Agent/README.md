# Poetry Analysis Agent System

## What I Built
This Python script implements a multi-agent poetry analysis system that:
1. Uses a main "Poetry Analyser" agent to classify poems
2. Handles specialized analysis via 3 sub-agents:
   - Lyric poetry expert
   - Narrative poetry expert 
   - Dramatic poetry expert
3. Implements handoff functionality between agents
4. Uses Gemini's AI model 

## Key Components

### Core Features
- **Agent Specialization**: Each agent has domain-specific knowledge about different poetry types
- **Intelligent Routing**: Main agent analyzes poems and routes to appropriate specialist
- **Handoff System**: Clean transfer between agents with reason tracking
- **Async Execution**: Uses asyncio for efficient AI model calls

### Technical Implementation
- OpenAI Agent SDK framework 
- Gemini API integration 
- Pydantic models for type-safe handoff data
- Environment variable configuration

## What I Learned
1. **Multi-agent Architecture**: How to design specialized agents that collaborate
2. **Handoff Patterns**: Implementing context transfer between agents

## Usage
1. Set `GEMINI_API_KEY` in .env
2. Run with `uv run main.py`
3. The system will analyze the sample dramatic poetry line from Julius Caesar

Example output shows:
- Which specialist agent was selected
- The reasoning for handoff
- Final analysis output

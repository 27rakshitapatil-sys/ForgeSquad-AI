# Agent Orchestration System

A multi-agent system where a Supervisor delegates work to specialist agents,
with tool use, persistent memory, and human-in-the-loop approval.

## Features
- **Supervisor delegation**: an LLM decides which agent works next (LangGraph)
- **Specialist agents**: Researcher and Writer, each with its own role
- **Tool use**: agents can call Python functions (calculator, clock)
- **Persistent memory**: past runs are saved in SQLite and reused as background
- **Human-in-the-loop**: the graph pauses for approval before the Writer runs
- **Web UI**: Streamlit page with Approve / Reject buttons

## Tech Stack
Python, LangGraph, Google Gemini, SQLite, Streamlit

## How to Run
1. Create a virtual environment and install packages:
   `pip install langgraph google-genai python-dotenv streamlit`
2. Create a `.env` file containing: `GEMINI_API_KEY=your-key`
3. Start the app: `streamlit run ui.py`

## Roadmap
- Reviewer agent
- PostgreSQL + ChromaDB for memory
- Redis + Celery for background runs
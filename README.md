# LangGraph Stateless Chatbot — Test Task

This repo contains a simple LangGraph stateless chat bot with a tool that returns the current UTC time.

## Task Description

- A stateless chat graph using LangGraph where the bot replies to each user message.
- An agent with a single tool: `get_current_time` that returns current UTC time in ISO‑8601 format.
- The bot calls this tool when the user asks for the time, e.g., “What time is it?”
- Launch the bot with `langgraph dev`.
- Minimal repo: one Python file, `requirements.txt`, and this README.

## Setup & Run

```bash
git clone <your-repo-url>
cd <your-repo-folder>

python -m venv .venv
source .venv/bin/activate   

pip install -r requirements.txt

langgraph dev
# langgraph-weather

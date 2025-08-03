# 🤖 Console-Based Support Agent System

A multi-agent customer support system built with the OpenAI Agents SDK that runs in the console. It intelligently routes user queries (e.g., billing, technical, general) to specialized agents and executes relevant tools based on context.

---

## 🎯 Objective

Simulate a real-world support flow with agent handoffs, context sharing, and conditional tool execution.

---

## 🛠️ Features

- **3+ Agents**:
  - `TriageAgent`: Determines query type and routes to the right agent.
  - `BillingAgent`: Handles refunds and billing issues.
  - `TechAgent`: Handles technical problems.
  - *(Optional)* `GeneralAgent`: For other inquiries.

- **Tools with Conditions**:
  - `refund()` → Only available if `is_premium_user == True`.
  - `restart_service()` → Only if `issue_type == "technical"`.

- **Agent Handoff**:
  - Dynamic routing based on user message and extracted issue type.

- **Context Management**:
  - Uses `Pydantic` model to pass and share user details (`name`, `is_premium_user`, `issue_type`) between agents.

- **CLI Interface**:
  - Runs entirely in the terminal.
  - Interactive input/output loop.

- **Optional Bonus**:
  - OutputGuardrail (removes apology statements like "sorry").
  - Tool execution logs via `stream_events()`.

---

## 🚀 Usage

1. Setup Commands:

```bash
uv init project-name
cd project-name
uv add openai-agents python-dotenv
```

## Run the system:

```bash
uv run main.py
```

## Follow the CLI prompts:

Enter your name

State if you're a premium user

Ask your question (e.g., "I want a refund.")

---------------------------------------------------------------

**Build with ❤ by [Faria Mustaqim](https://github.com/Zaibunis)**




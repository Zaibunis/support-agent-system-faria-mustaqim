from openai import OpenAI
from agents import Agent, Runner, function_tool, OutputGuardrail
from pydantic import BaseModel
import re
from connection import config

# === Step 1: Define the shared context model ===
class SupportContext(BaseModel):
    user_id: str
    name: str
    is_premium_user: bool
    issue_type: str


# === Step 2: Define Tools ===

@function_tool
def refund(context: SupportContext) -> str:
    return f"✅ Refund processed for premium user {context.name}."

refund.is_enabled = lambda ctx: ctx.get("is_premium_user", False)


@function_tool
def restart_service(context: SupportContext) -> str:
    return f"🔁 Service restarted for user {context.name}."

restart_service.is_enabled = lambda ctx: ctx.get("issue_type") == "technical"


@function_tool
def faq_answer(context: SupportContext) -> str:
    return f"📄 General FAQ answer provided to {context.name}."


# === Step 3: Define Specialized Agents ===

billing_agent = Agent(
    name="BillingAgent",
    instructions="Handle all billing-related questions.",
    tools=[refund],
)

tech_agent = Agent(
    name="TechAgent",
    instructions="Handle technical issues like internet problems.",
    tools=[restart_service],
)

general_agent = Agent(
    name="GeneralAgent",
    instructions="Handle general, non-technical, non-billing queries.",
    tools=[faq_answer],
)


# === Step 4: Triage Agent ===

def classify_issue(query: str) -> str:
    if "refund" in query:
        return "billing"
    elif re.search(r"(restart|internet|slow)", query):
        return "technical"
    else:
        return "general"

triage_agent = Agent(
    name="TriageAgent",
    instructions="Route user requests to the correct specialized agent based on the issue type.",
)


@function_tool
def route_user(context: SupportContext, query: str) -> str:
    issue_type = classify_issue(query)
    context.issue_type = issue_type
    print(f"\n🧠 Triage determined issue type: {issue_type.upper()}")

    if issue_type == "billing":
        return billing_agent.invoke(context=context)
    elif issue_type == "technical":
        return tech_agent.invoke(context=context)
    else:
        return general_agent.invoke(context=context)

triage_agent.tools = [route_user]


# === Step 6: CLI Interface ===

def run_console_support_agent():
    print("🛠️  Welcome to the Console Support Agent System!")
    print("Type 'exit' to quit.\n")

    name = input("Enter your name: ")
    is_premium = input("Are you a premium user? (yes/no): ").strip().lower() == "yes"

    while True:
        query = input(f"\n{name}, how can we assist you today? > ")
        if query.lower() == "exit":
            print("👋 Goodbye!")
            break

        # Inject context
        context = {
            "user_id": "001",
            "name": name,
            "is_premium_user": is_premium,
        }

        # Invoke triage agent with query
        response = triage_agent.invoke(context=context, query=query)

        # Print response directly (guardrail removed)
        print(f"\n🤖 Response:\n{response}")


# === Step 7: Script Entry Point ===
if __name__ == "__main__":
    run_console_support_agent()

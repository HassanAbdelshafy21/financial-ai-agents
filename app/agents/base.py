# app/agents/base.py
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create_openai_functions_agent, tool


# Define tools
@tool
def savings_calculator(amount: float, months: int) -> str:
    """Calculate total savings if saving 'amount' every month for 'months' months."""
    total = amount * months
    return f"You will save ${total} in {months} months."


tools = [savings_calculator]

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini")  # Use your preferred model

# Pull default agent prompt
prompt = hub.pull("hwchase17/openai-functions-agent")

# Create agent
agent = create_openai_functions_agent(llm, tools, prompt)

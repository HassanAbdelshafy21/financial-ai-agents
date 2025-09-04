from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool


@tool
def savings_calculator(amount: float, months: int) -> str:
    """Calculate savings for a given monthly amount and months."""
    return f"Total savings after {months} months: ${amount * months}"


llm = ChatOpenAI(model="gpt-4o-mini")  # requires OPENAI_API_KEY
agent = create_react_agent(llm, [savings_calculator])

if __name__ == "__main__":
    response = agent.invoke(
        {
            "messages": [
                ("user", "If I save 200 per month for 12 months, how much will I have?")
            ]
        }
    )
    print(response)

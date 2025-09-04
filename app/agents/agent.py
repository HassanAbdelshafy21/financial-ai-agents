from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from app.core.config import settings


@tool
def savings_calculator(amount: float, months: int) -> str:
    """Calculate savings for a given monthly amount and months."""
    return f"Total savings after {months} months: ${amount * months}"


@tool
def compound_interest(
    principal: float, monthly_contrib: float, annual_rate: float, years: int
) -> str:
    """
    Calculate compound interest with monthly contributions.
    principal = initial amount
    monthly_contrib = amount added each month
    annual_rate = annual interest rate in percent (e.g. 5 for 5%)
    years = investment duration in years
    """
    r = annual_rate / 100 / 12  # monthly rate
    months = years * 12
    future_value = principal * (1 + r) ** months
    for _ in range(months):
        future_value = (future_value + monthly_contrib) * (1 + r)
    return f"Future value after {years} years: ${future_value:,.2f}"


# LLM
llm = ChatOpenAI(model="gpt-4o-mini", api_key=settings.OPENAI_API_KEY)

# Agent with multiple tools
agent = create_react_agent(llm, [savings_calculator, compound_interest])

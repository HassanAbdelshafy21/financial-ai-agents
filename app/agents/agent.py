from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from app.core.config import settings
import math
from langgraph.checkpoint.memory import MemorySaver
from typing import List, Dict


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


@tool
def loan_payment_calculator(
    principal: float, annual_rate: float, years: int
) -> str:
    """
    Calculate monthly loan payment using standard amortization formula.
    principal = loan amount
    annual_rate = annual interest rate in percent (e.g. 5 for 5%)
    years = loan term in years
    """
    if annual_rate == 0:
        monthly_payment = principal / (years * 12)
        return f"Monthly payment (0% interest): ${monthly_payment:,.2f}"
    
    r = annual_rate / 100 / 12  # monthly rate
    n = years * 12  # total payments
    monthly_payment = principal * (r * (1 + r)**n) / ((1 + r)**n - 1)
    total_paid = monthly_payment * n
    total_interest = total_paid - principal
    
    return f"Monthly payment: ${monthly_payment:,.2f}\nTotal paid: ${total_paid:,.2f}\nTotal interest: ${total_interest:,.2f}"


@tool
def portfolio_analyzer(investments: str) -> str:
    """
    Analyze investment portfolio allocation and risk.
    investments = comma-separated list like "stocks:60,bonds:30,cash:10"
    """
    try:
        allocations = {}
        total = 0
        for item in investments.split(','):
            asset, percent = item.strip().split(':')
            percent = float(percent)
            allocations[asset.strip()] = percent
            total += percent
        
        if abs(total - 100) > 0.1:
            return f"Warning: Allocations total {total}%, should equal 100%"
        
        risk_scores = {
            'stocks': 8, 'equities': 8, 'crypto': 10, 'cryptocurrency': 10,
            'bonds': 4, 'treasuries': 2, 'cash': 1, 'savings': 1,
            'reits': 6, 'real estate': 6, 'commodities': 7
        }
        
        portfolio_risk = sum(allocations.get(asset, 0) * risk_scores.get(asset.lower(), 5) for asset in allocations) / 100
        
        risk_level = "Conservative" if portfolio_risk <= 3 else "Moderate" if portfolio_risk <= 6 else "Aggressive"
        
        analysis = f"Portfolio Analysis:\n"
        for asset, percent in allocations.items():
            analysis += f"- {asset.title()}: {percent}%\n"
        analysis += f"\nRisk Level: {risk_level} ({portfolio_risk:.1f}/10)\n"
        
        if portfolio_risk > 7:
            analysis += "Recommendation: Consider reducing high-risk investments for better balance"
        elif portfolio_risk < 3:
            analysis += "Recommendation: Consider adding growth investments for better returns"
        
        return analysis
        
    except Exception as e:
        return f"Error parsing portfolio. Use format: 'stocks:60,bonds:30,cash:10'"


@tool
def budget_planner(income: float, expenses: str) -> str:
    """
    Analyze monthly budget and provide recommendations.
    income = monthly income
    expenses = comma-separated list like "rent:1200,food:500,transport:300"
    """
    try:
        expense_dict = {}
        total_expenses = 0
        
        for item in expenses.split(','):
            category, amount = item.strip().split(':')
            amount = float(amount)
            expense_dict[category.strip()] = amount
            total_expenses += amount
        
        remaining = income - total_expenses
        savings_rate = (remaining / income) * 100 if income > 0 else 0
        
        budget_analysis = f"Budget Analysis:\n"
        budget_analysis += f"Monthly Income: ${income:,.2f}\n"
        budget_analysis += f"Total Expenses: ${total_expenses:,.2f}\n"
        budget_analysis += f"Remaining: ${remaining:,.2f}\n"
        budget_analysis += f"Savings Rate: {savings_rate:.1f}%\n\n"
        
        budget_analysis += "Expense Breakdown:\n"
        for category, amount in expense_dict.items():
            percentage = (amount / income) * 100 if income > 0 else 0
            budget_analysis += f"- {category.title()}: ${amount:,.2f} ({percentage:.1f}%)\n"
        
        if savings_rate < 10:
            budget_analysis += "\n⚠️  Low savings rate. Consider reducing discretionary spending."
        elif savings_rate > 20:
            budget_analysis += "\n✅ Excellent savings rate! Consider investing surplus."
        
        return budget_analysis
        
    except Exception as e:
        return f"Error parsing budget. Use format: 'rent:1200,food:500,transport:300'"


@tool
def retirement_calculator(
    current_age: int, retirement_age: int, current_savings: float, 
    monthly_contribution: float, annual_return: float
) -> str:
    """
    Calculate retirement savings projection.
    current_age = your current age
    retirement_age = desired retirement age
    current_savings = current retirement savings
    monthly_contribution = monthly contribution amount
    annual_return = expected annual return in percent (e.g. 7 for 7%)
    """
    years_to_retire = retirement_age - current_age
    if years_to_retire <= 0:
        return "You're already at or past retirement age!"
    
    r = annual_return / 100 / 12  # monthly rate
    months = years_to_retire * 12
    
    # Future value of current savings
    future_current = current_savings * (1 + annual_return/100) ** years_to_retire
    
    # Future value of monthly contributions
    if r > 0:
        future_contributions = monthly_contribution * (((1 + r) ** months - 1) / r)
    else:
        future_contributions = monthly_contribution * months
    
    total_retirement = future_current + future_contributions
    
    # 4% withdrawal rule estimate
    annual_income = total_retirement * 0.04
    monthly_income = annual_income / 12
    
    result = f"Retirement Projection ({years_to_retire} years):\n"
    result += f"Total at retirement: ${total_retirement:,.2f}\n"
    result += f"Estimated annual income (4% rule): ${annual_income:,.2f}\n"
    result += f"Estimated monthly income: ${monthly_income:,.2f}\n\n"
    
    # Recommendations
    if monthly_income < monthly_contribution * 10:  # Rule of thumb
        result += "⚠️  Consider increasing contributions for better retirement income."
    else:
        result += "✅ You're on track for a comfortable retirement!"
    
    return result


@tool
def debt_payoff_calculator(debt_amount: float, interest_rate: float, payment_strategies: str) -> str:
    """
    Compare debt payoff strategies.
    debt_amount = total debt amount
    interest_rate = annual interest rate in percent
    payment_strategies = comma-separated payments like "minimum:200,aggressive:400"
    """
    try:
        strategies = {}
        for strategy in payment_strategies.split(','):
            name, payment = strategy.strip().split(':')
            strategies[name.strip()] = float(payment)
        
        r = interest_rate / 100 / 12  # monthly rate
        results = []
        
        for strategy_name, monthly_payment in strategies.items():
            if monthly_payment <= debt_amount * r:
                results.append(f"{strategy_name}: Payment too low to cover interest!")
                continue
                
            balance = debt_amount
            months = 0
            total_paid = 0
            
            while balance > 0 and months < 600:  # 50 year max
                interest_payment = balance * r
                principal_payment = min(monthly_payment - interest_payment, balance)
                balance -= principal_payment
                total_paid += monthly_payment
                months += 1
                
                if balance <= 0:
                    break
            
            years = months / 12
            interest_paid = total_paid - debt_amount
            
            results.append(f"{strategy_name.title()}: {months} months ({years:.1f} years)")
            results.append(f"  Total paid: ${total_paid:,.2f}")
            results.append(f"  Interest paid: ${interest_paid:,.2f}\n")
        
        return "Debt Payoff Comparison:\n" + "\n".join(results)
        
    except Exception as e:
        return f"Error parsing strategies. Use format: 'minimum:200,aggressive:400'"


@tool
def emergency_fund_calculator(monthly_expenses: float, current_savings: float, target_months: int = 6) -> str:
    """
    Calculate emergency fund requirements and progress.
    monthly_expenses = your monthly expenses
    current_savings = current emergency savings
    target_months = months of expenses to save (default 6)
    """
    target_amount = monthly_expenses * target_months
    remaining_needed = max(0, target_amount - current_savings)
    coverage_months = current_savings / monthly_expenses if monthly_expenses > 0 else 0
    
    result = f"Emergency Fund Analysis:\n"
    result += f"Monthly expenses: ${monthly_expenses:,.2f}\n"
    result += f"Target fund ({target_months} months): ${target_amount:,.2f}\n"
    result += f"Current savings: ${current_savings:,.2f}\n"
    result += f"Current coverage: {coverage_months:.1f} months\n"
    result += f"Still needed: ${remaining_needed:,.2f}\n\n"
    
    if coverage_months < 3:
        result += "⚠️  Critical: Build emergency fund immediately!"
    elif coverage_months < 6:
        result += "⚠️  Warning: Increase emergency fund when possible."
    else:
        result += "✅ Great! You have adequate emergency coverage."
    
    if remaining_needed > 0:
        for monthly_save in [100, 250, 500]:
            months_to_target = remaining_needed / monthly_save
            result += f"\nSaving ${monthly_save}/month: {months_to_target:.1f} months to target"
    
    return result


@tool
def tax_calculator(income: float, filing_status: str = "single", state: str = "none") -> str:
    """
    Estimate federal income tax (simplified US tax calculation).
    income = annual gross income
    filing_status = single, married_joint, married_separate, head_of_household
    state = state name or 'none' for federal only
    """
    # 2024 tax brackets (single filer)
    brackets_single = [
        (11000, 0.10), (44725, 0.12), (95375, 0.22), 
        (182050, 0.24), (231250, 0.32), (578125, 0.35), (float('inf'), 0.37)
    ]
    
    brackets_married = [
        (22000, 0.10), (89450, 0.12), (190750, 0.22), 
        (364200, 0.24), (462500, 0.32), (693750, 0.35), (float('inf'), 0.37)
    ]
    
    standard_deductions = {
        "single": 13850, "married_joint": 27700, 
        "married_separate": 13850, "head_of_household": 20800
    }
    
    brackets = brackets_married if "married_joint" in filing_status else brackets_single
    standard_deduction = standard_deductions.get(filing_status, 13850)
    
    taxable_income = max(0, income - standard_deduction)
    
    tax = 0
    prev_bracket = 0
    
    for bracket_limit, rate in brackets:
        taxable_in_bracket = min(taxable_income, bracket_limit) - prev_bracket
        if taxable_in_bracket <= 0:
            break
        tax += taxable_in_bracket * rate
        prev_bracket = bracket_limit
        if taxable_income <= bracket_limit:
            break
    
    effective_rate = (tax / income * 100) if income > 0 else 0
    marginal_rate = next((rate * 100 for limit, rate in brackets if taxable_income <= limit), 37)
    
    result = f"Tax Estimate ({filing_status}):\n"
    result += f"Gross income: ${income:,.2f}\n"
    result += f"Standard deduction: ${standard_deduction:,.2f}\n"
    result += f"Taxable income: ${taxable_income:,.2f}\n"
    result += f"Federal tax: ${tax:,.2f}\n"
    result += f"After-tax income: ${income - tax:,.2f}\n"
    result += f"Effective rate: {effective_rate:.1f}%\n"
    result += f"Marginal rate: {marginal_rate:.0f}%\n"
    
    if state != "none":
        result += f"\nNote: State taxes for {state} not included in calculation."
    
    return result


# LLM
llm = ChatOpenAI(model="gpt-4o-mini", api_key=settings.OPENAI_API_KEY)
# Create checkpointer  
checkpointer = MemorySaver()

# Agent with all financial tools
agent = create_react_agent(llm, [
    savings_calculator,
    compound_interest, 
    loan_payment_calculator,
    portfolio_analyzer,
    budget_planner,
    retirement_calculator,
    debt_payoff_calculator,
    emergency_fund_calculator,
    tax_calculator
,], checkpointer=checkpointer)

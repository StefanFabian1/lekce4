from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from dotenv import load_dotenv
import os
import logging
from typing import Union, Dict
import math

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

def validate_inputs(principal: float = None, rate: float = None, years: float = None, 
                   equities: float = None, bonds: float = None, cash: float = None) -> Dict:
    """Validate input parameters and return error messages if any."""
    errors = []
    
    if principal is not None and principal <= 0:
        errors.append("Výška investície musí byť kladné číslo.")
    
    if rate is not None and rate < 0:
        errors.append("Úroková sadzba nemôže byť záporná.")
    
    if years is not None:
        if years <= 0:
            errors.append("Investičný horizont musí byť kladné číslo.")
        elif years < 0.1:  # Menej ako 1 mesiac
            errors.append("Minimálny investičný horizont je 1 mesiac.")
        elif years > 100:
            errors.append("Maximálny investičný horizont je 100 rokov.")
    
    if equities is not None and (equities < 0 or equities > 100):
        errors.append("Podiel akcií musí byť medzi 0% a 100%.")
    
    if bonds is not None and (bonds < 0 or bonds > 100):
        errors.append("Podiel obligácií musí byť medzi 0% a 100%.")
    
    if cash is not None and (cash < 0 or cash > 100):
        errors.append("Podiel hotovosti musí byť medzi 0% a 100%.")
    
    if equities is not None and bonds is not None and cash is not None:
        total = equities + bonds + cash
        if abs(total - 100) > 0.01:  # Povolíme malú odchýlku kvôli zaokrúhľovaniu
            errors.append(f"Súčet podielov musí byť 100% (aktuálne {total}%).")
    
    return {"is_valid": len(errors) == 0, "errors": errors}

def calculate_compound_interest(principal: float, rate: float, years: int) -> Dict:
    """Calculate compound interest and growth."""
    validation = validate_inputs(principal=principal, rate=rate, years=years)
    if not validation["is_valid"]:
        return {"error": validation["errors"]}
    
    final_amount = principal * (1 + rate) ** years
    total_interest = final_amount - principal
    
    return {
        "final_amount": round(final_amount, 2),
        "total_interest": round(total_interest, 2),
        "principal": principal,
        "annual_rate": rate,
        "years": years
    }

def calculate_portfolio_risk(equities: float, bonds: float, cash: float) -> Dict:
    """Calculate portfolio risk based on asset allocation."""
    validation = validate_inputs(equities=equities, bonds=bonds, cash=cash)
    if not validation["is_valid"]:
        return {"error": validation["errors"]}
    
    risk_score = (equities * 0.8 + bonds * 0.3 + cash * 0.1) / 100
    
    return {
        "risk_score": round(risk_score, 2),
        "risk_level": "High" if risk_score > 0.6 else "Medium" if risk_score > 0.3 else "Low",
        "equities": equities,
        "bonds": bonds,
        "cash": cash
    }

def compare_investment_options(amount: float, years: int) -> Dict:
    """Compare different investment options."""
    validation = validate_inputs(principal=amount, years=years)
    if not validation["is_valid"]:
        return {"error": validation["errors"]}
    
    returns = {
        "savings_account": 0.02,  # 2% annual return
        "bonds": 0.04,            # 4% annual return
        "stocks": 0.08,           # 8% annual return
        "real_estate": 0.06       # 6% annual return
    }
    
    results = {}
    for option, rate in returns.items():
        final = amount * (1 + rate) ** years
        results[option] = {
            "final_amount": round(final, 2),
            "total_return": round(final - amount, 2),
            "annual_rate": rate
        }
    
    return results

# Define tools
tools = [
    calculate_compound_interest,
    calculate_portfolio_risk,
    compare_investment_options
]

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)
llm_with_tools = llm.bind_tools(tools)

# System message
sys_msg = SystemMessage(content="""You are an investment advisor assistant. You can:
1. Calculate compound interest and investment growth
2. Analyze portfolio risk based on asset allocation
3. Compare different investment options
4. Provide investment recommendations based on risk tolerance
5. Explain investment concepts and strategies

Always:
- Explain your calculations clearly
- Consider risk tolerance in recommendations
- Provide balanced advice
- Use real-world examples when possible
- Highlight both potential returns and risks
- Validate inputs and provide clear error messages
- Handle edge cases gracefully

If you receive invalid inputs:
- Explain why the input is invalid
- Provide guidance on correct input format
- Suggest reasonable alternatives

If you receive unrelated questions:
- Politely explain your limitations
- Redirect to appropriate resources

Example interaction:
User: "What's the best investment for $10,000 over 5 years?"
Assistant: Let me analyze different options for you.

1. Savings Account (Low Risk):
   - Final amount: $11,040
   - Total return: $1,040
   - Annual return: 2%

2. Bonds (Medium Risk):
   - Final amount: $12,167
   - Total return: $2,167
   - Annual return: 4%

3. Stocks (Higher Risk):
   - Final amount: $14,693
   - Total return: $4,693
   - Annual return: 8%

Recommendation:
Based on your investment horizon of 5 years, I would recommend a balanced approach:
- 60% in stocks for growth
- 30% in bonds for stability
- 10% in cash for liquidity

This allocation would give you a moderate risk level while aiming for reasonable returns. Would you like me to calculate the expected returns for this specific allocation?""")

# Node
def assistant(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

# Build graph
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    tools_condition,
)
builder.add_edge("tools", "assistant")

# Compile graph
graph = builder.compile()

def get_initial_state() -> MessagesState:
    """Create initial state with system message"""
    return {"messages": [sys_msg]}

if __name__ == "__main__":
    logger.info("Starting Investment Advisor Assistant...")
    print("\nInvestment Advisor ready! Type 'quit' to exit.")
    print("Example commands:")
    print("- Calculate returns for $10,000 at 5% for 10 years")
    print("- What's my portfolio risk with 60% stocks, 30% bonds, 10% cash?")
    print("- Compare investment options for $50,000 over 5 years")
    print("- Explain diversification\n")
    
    state = get_initial_state()
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() == 'quit':
                print("\nGoodbye!")
                break
                
            state["messages"].append(HumanMessage(content=user_input))
            state = graph.invoke(state)
            print(f"\nAssistant: {state['messages'][-1].content}")
            
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            print("\nSorry, I encountered an error. Please try again.")
            state = get_initial_state() 
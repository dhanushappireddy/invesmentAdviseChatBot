from App.ollama_utils import callOllama
# from App.Tenure import calculate_tenure_years_months_String
from App.Tenure import calculate_expectedAmount
from App.main import getUserDetails
from App.predict import predict
from App.ReturnPercentage import calculateReturn
MODEL_NAME = "gemma3"
def analyzeData(name: str, age: int, investmentAmount: float, tenure: float, salary: float, riskTolerance: str) -> str:
    relevant_data,Return_Amount, Return_Percentage = getUserDetails(name, age, investmentAmount, tenure, riskTolerance)
    context = "\n\n".join(relevant_data)
    avgStocksReturn = calculateReturn("stocks")
    avgMutualFunds = calculateReturn("mutualfunds")
    avgFD = calculateReturn("fd")
    avgGold = calculateReturn("gold")
    prompt1 = f"""
        You are a professional financial advisor.
        Based on these predictions:
        Expected return Amount: {Return_Amount} 
        Expected return percentage: {Return_Percentage}
        context: {context}
        A user has provided the following personal, financial details and consider examples: 
        - Name: {name}
        - Age: {age}
        - Annual Salary: {salary}
        - Current Investment Amount: {investmentAmount}
        - Tenure of investment in years: {tenure}
        - Risk Tolerance: {riskTolerance}
        
        The user is open to investing in the following asset classes, each with its own expected annual return and investment tenure to acheieve his expected amount:
        1. Mutual Funds: {avgMutualFunds}% return annually, Expected Amount in the give tenure: {calculate_expectedAmount(investmentAmount, tenure, 12)}
        2. Stocks: {avgStocksReturn}% return annually, Expected Amount in the give tenure: {calculate_expectedAmount(investmentAmount, tenure, 15)}
        3. Gold: {avgGold}% return annually, Expected Amount in the give tenure: {calculate_expectedAmount(investmentAmount, tenure, 10)}
        5. Fixed Deposits: {avgFD}% return annually, Expected Amount in the give tenure: {calculate_expectedAmount(investmentAmount, tenure, 7)}

        Please analyze the user’s financial profile, risk appetite (inferred from age, salary and risk tolerance). From given predictions and that context, generate a personalized investment strategy.

        Respond in JSON format inside suggested_allocation considering the risk tolerance and suggest:
        {{
            "strategy_summary": "...",
            "recommended_assets": ["..."],
            "risk_notes": "...",
            "suggested_allocation": "...%"
        }}
    """
    prompt = f"""
        You are a professional financial advisor.
        Based on these examples:
        context: {context}
        A user has provided the following personal, financial details and consider examples: 
        - Name: {name}
        - Age: {age}
        - Annual Salary: {salary}
        - Current Investment Amount: {investmentAmount}
        - Tenure of investment in years: {tenure}
        - Risk Tolerance: {riskTolerance}
        
        The user is open to investing in the following asset classes, each with its own expected annual return and investment tenure to acheieve his expected amount:
        1. Mutual Funds: {avgMutualFunds}% return annually, Expected Amount in the give tenure: {calculate_expectedAmount(investmentAmount, tenure, 12)}
        2. Stocks: {avgStocksReturn}% return annually, Expected Amount in the give tenure: {calculate_expectedAmount(investmentAmount, tenure, 15)}
        3. Gold: {avgGold}% return annually, Expected Amount in the give tenure: {calculate_expectedAmount(investmentAmount, tenure, 10)}
        5. Fixed Deposits: {avgFD}% return annually, Expected Amount in the give tenure: {calculate_expectedAmount(investmentAmount, tenure, 7)}

        Please analyze the user’s financial profile, risk appetite (inferred from age, salary and risk tolerance). From given predictions and that context, generate a personalized investment strategy.

        Respond in JSON format inside suggested_allocation considering the risk tolerance and suggest:
        {{
            "strategy_summary": "...",
            "recommended_assets": ["..."],
            "risk_notes": "...",
            "suggested_allocation": "...%"
        }}
    """
    
    print(prompt1)
    return callOllama(MODEL_NAME, prompt1)




import json
import re
import pandas as pd
import streamlit as st
import time
import requests
import sys
import os

# Get the absolute path to the parent directory (App)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to sys.path if it's not already there
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
from App.Tenure import calculate_percentage_return
from App.Tenure import calculate_expectedAmount
from App.ReturnPercentage import calculateReturn
#Page Title

# Set the page title
st.set_page_config(page_title="Investment ChatBot Advisor")

# App title
st.title("Investment Advice Chat Bot 🤖")# Creating fields
# ---- Define clear function for session state ----
def clear_all():
    st.session_state.user_input = ""
    st.session_state.user_age = 25
    st.session_state.user_salary_earning = 10000
    st.session_state.user_investment_amount = 0
    st.session_state.user_tenure = 0
    st.session_state.system_investment_plan = ""

def checkAllFieldsEntered():
    if (st.session_state.user_input.strip() == "" and st.session_state.user_age == 0 and
        st.session_state.user_salary_earning <= 0 and st.session_state.user_investment_amount <= 0 and
        st.session_state.user_tenure <=0):
        st.warning("Please fill all the fields.")
        return False
    elif st.session_state.user_input.strip() == "":
        st.warning("Please enter your name.")
        return False
    elif st.session_state.user_age is None or st.session_state.user_age == 0:
        st.warning("Please select a valid age.")
        return False
    elif st.session_state.user_salary_earning is None or st.session_state.user_salary_earning <= 0:
        st.warning("Please enter a valid salary amount.")
        return False
    elif st.session_state.user_investment_amount is None or st.session_state.user_investment_amount <= 100:
        st.warning("Please enter a valid investment amount.")
        return False
    elif st.session_state.user_tenure is None or st.session_state.user_tenure == 0:
        st.warning("Please enter a valid tenure.")
        return False
    return True

st.text_input("Name", key="user_input",max_chars = 30,placeholder="Enter your name")
st.slider("Age", 0, 100, 25,key="user_age")
st.number_input("Salary Earning(per year)",0,10000000,10000,key="user_salary_earning")
st.number_input("Investment Amount",key="user_investment_amount")
st.slider("Tenure in years", 0, 30, 1,key="user_tenure")
st.selectbox("Risk Factor",("Low","Medium","High"),key="user_risk_factor")
col1, col2 = st.columns([1, 1])
# ---- Button Row Just Below Expected Amount ----
left_col, right_col = st.columns([1, 1])

with left_col:
    analyze_clicked = st.button("Analyse", use_container_width=True)

with right_col:
    clear_clicked = st.button("Clear", use_container_width=True)
if analyze_clicked:
    if checkAllFieldsEntered():
        with st.spinner("Analysing... 🤔"):
            st.session_state.inputValue = {
            "name": st.session_state.user_input,
            "age": st.session_state.user_age,
            "salary": st.session_state.user_salary_earning,
            "investmentAmount": st.session_state.user_investment_amount,
            "tenure": st.session_state.user_tenure,
            "riskTolerance": st.session_state.user_risk_factor
            }
            response = requests.post("http://localhost:8001/analyze", json= st.session_state.inputValue)
            # Check if the response is successful
            if response.status_code == 200:
                result = response.json() 
                response_value = result.get("response", "No response key found")
                print(response_value)
                response_string = result.get('response', '')
                # Remove extra newlines and other unwanted characters (e.g., extra spaces, tabs)
                cleaned_response_string = response_string.replace("\n", "").strip()
                # Parse the cleaned string to get the actual JSON object
                parsed_response = json.loads(cleaned_response_string)
                strategy_summary = parsed_response.get("strategy_summary", "No strategy summary found.")
                recommended_assets = parsed_response.get("recommended_assets", [])
                risk_notes = parsed_response.get("risk_notes", "No risk notes found.")
                suggested_allocation = parsed_response.get("suggested_allocation", "")
                
                # Prepare the result text to display
                result_text = ""
                for allocation in suggested_allocation.strip().split(","):
                    result_text += f"{allocation}\n"
                result_text += f"\n<strong>📊📊 Investment Strategy Overview:</strong>\n{strategy_summary}\n\n"
                # result_text += f"⚠️⚠️ Risk ⚠️⚠️ \n{risk_notes}"
                print(result_text)
                tenure = st.session_state.user_tenure
                investmentAmount = st.session_state.user_investment_amount
                avgStocksReturn = calculateReturn("stocks")
                avgMutualFunds = calculateReturn("mutualfunds")
                avgFD = calculateReturn("fd")
                avgGold = calculateReturn("gold")
                print(avgStocksReturn, avgMutualFunds, avgFD, avgGold)
                returnAmountMutalFunds = calculate_expectedAmount(st.session_state.inputValue["investmentAmount"], st.session_state.inputValue["tenure"], avgMutualFunds)
                returnAmountStocks = calculate_expectedAmount(st.session_state.inputValue["investmentAmount"], st.session_state.inputValue["tenure"], avgStocksReturn)
                returnAmountFD = calculate_expectedAmount(st.session_state.inputValue["investmentAmount"], st.session_state.inputValue["tenure"], avgFD)
                returnAmountGold = calculate_expectedAmount(st.session_state.inputValue["investmentAmount"], st.session_state.inputValue["tenure"], avgGold)
                data = {
                    "Asset Class": ["Mutual Funds", "Stocks", "Fixed Deposit", "Gold"],
                    "Invested Amount(₹)": [investmentAmount, investmentAmount, investmentAmount, investmentAmount],
                    "Expected Return per year(%)": [avgMutualFunds, avgStocksReturn, avgFD, avgGold],
                    f"Expected Amount(₹) within {tenure} years": [returnAmountMutalFunds, returnAmountStocks, returnAmountFD, returnAmountGold],
                    "Total gains(%)": [calculate_percentage_return(investmentAmount, returnAmountMutalFunds), calculate_percentage_return(investmentAmount, returnAmountStocks), calculate_percentage_return(investmentAmount, returnAmountFD), calculate_percentage_return(investmentAmount, returnAmountGold)]
                }
                # Create DataFrame
                df = pd.DataFrame(data)
                def generate_centered_table(df):
                    html = """
                    <style>
                        table {
                            width: 100%;
                            border-collapse: collapse;
                        }
                        th, td {
                            text-align: center;
                            padding: 10px;
                            border: 1px solid #ccc;
                        }
                        th {
                            background-color: #f2f2f2;
                            font-weight: bold;
                        }
                    </style>
                    <table>
                        <thead>
                            <tr>""" + "".join(f"<th>{col}</th>" for col in df.columns) + "</tr>" + """
                        </thead>
                        <tbody>
                    """

                    for _, row in df.iterrows():
                        html += "<tr>" + "".join(f"<td>{val}</td>" for val in row) + "</tr>"

                    html += "</tbody></table>"
                    return html

                # Display in Streamlit
                st.title("Investment Options")
                st.markdown(generate_centered_table(df), unsafe_allow_html=True)
                # to display investment strategy
                # Convert line breaks to HTML <br> for proper rendering
                html_result = result_text.replace("\n", "<br>")

                # Display using st.markdown
                st.markdown(f"""
                <div style="margin-top:20px; padding:15px; background-color:#f0f8ff; 
                            border-left:4px solid #009879; font-family:Arial; font-size:16px;">
                    <strong>💡 Recommendation:</strong><br>
                    {html_result}
                </div>
                """, unsafe_allow_html=True)
                st.markdown("""
        <div style="margin-top:20px; padding:15px; font-size:16px; background-color:#fff3f3; 
                    border:1px solid #f2b0b0; text-align:center; color:#d63333; font-family: Arial, sans-serif; 
                    border-radius:5px;">
            <strong>Disclaimer:</strong> Always consult with a financial advisor before making investment decisions.
        </div>
    """, unsafe_allow_html=True)
                #st.text_area("Investment Plan", result, height=300,key="system_investment_plan")
            else:
                st.error(f"Error: Received status code {response.status_code}")
    else:
        st.warning("Please fill in all the fields correctly before analyzing.")
if clear_clicked:
        st.button("Clear", on_click=clear_all)
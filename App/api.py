from fastapi import FastAPI, Body
from pydantic import BaseModel
import sys
import os

# Get the absolute path to the parent directory (App)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to sys.path if it's not already there
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
from App.processor import analyzeData
from App.Tenure import calculate_tenure_years_months
app = FastAPI()
print(f"FastAPI app instance created: {app}")  # Add this line
# Define a simple GET endpoint to verify the server is up and running
class AnalyzeRequest(BaseModel):
    name: str
    age: int
    salary: float
    investmentAmount: float
    tenure: int
    riskTolerance: str
@app.get("/")
async def read_root():
    return {"message": "Hi Hello."}
@app.post("/analyze/")
async def analyze(request: AnalyzeRequest):
    print("Called successfully")
    # Extract the transcript from the request body
    name = request.name 
    age = request.age
    salary = request.salary
    investmentAmount = request.investmentAmount
    riskTolerance = request.riskTolerance
    tenure = request.tenure
    response = analyzeData(name, age, investmentAmount, tenure, salary, riskTolerance)
    return {
        "response": response
    }

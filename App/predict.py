import joblib
import pandas as pd
import numpy as np

def predict(age, investmentAmount, tenure, risk):
    # Initialize the risk tolerance values to 0
    risk_Tolerance_Low = 0
    risk_Tolerance_Moderate = 0
    risk_Tolerance_High = 0
    
    # Set the values based on the given risk category
    if risk == "Low":
        risk_Tolerance_Low = 1
    elif risk == "Medium":
        risk_Tolerance_Moderate = 1
    elif risk == "High":
        risk_Tolerance_High = 1
    
    # Load the model for predicting Return_Amount
    model_amt = joblib.load("xgb_return_amount_model.pkl")
    model_percent = joblib.load("xgb_return_percentage_model.pkl")

    # Prepare the input data as a DataFrame
    new_data = pd.DataFrame([{
        'Age': age,
        'Investment_Amount': investmentAmount,
        'Tenure': tenure,
        'Risk_Tolerance_Low': risk_Tolerance_Low,
        'Risk_Tolerance_Moderate': risk_Tolerance_Moderate,
        'Risk_Tolerance_High': risk_Tolerance_High
    }])

    # Make the prediction (Log-transformed return amount)
    log_predicted_return = model_amt.predict(new_data)[0]
    predicted_percentage = model_percent.predict(new_data)[0]

    # Apply inverse transformation to get the actual return amount
    predicted_return = np.expm1(log_predicted_return)
    
    print("Predicted Return Amount:", predicted_return)
    print("Predict percentage return: ", predicted_percentage)
    return (predicted_return, predicted_percentage)

# if __name__ == "__main__":
#     # Example usage
#     predict(25, 100000, 1, "High")

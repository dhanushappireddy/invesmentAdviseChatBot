import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import xgboost as xgb
from xgboost import XGBRegressor
import joblib  # for saving/loading model
from pathlib import Path

# project_root = folder that contains "App" and "DataSets"
project_root = Path(__file__).resolve().parent.parent  

file_path = project_root / "DataSets" / "Datasets_Investment" / "investment_dataset.csv"

print("🔎 Looking for:", file_path)
print("✅ Exists:", file_path.exists())

df = pd.read_csv(file_path)

# 2. Preprocess the data
# One-hot encode the 'Risk_Tolerance' column
df = pd.get_dummies(df, columns=['Risk_Tolerance'], drop_first=False)

# Log transform 'Return_Amount' to handle large numbers
df['Log_Return_Amount'] = np.log1p(df['Return_Amount'])

# 3. Select input and output columns
# Inputs for model (Note: using one-hot encoded columns)
X = df[['Age', 'Investment_Amount', 'Tenure', 'Risk_Tolerance_Low', 'Risk_Tolerance_Moderate', 'Risk_Tolerance_High']]

# Output columns - we need two models: one for Return_Amount and one for Return_Percentage
y_amount = df['Log_Return_Amount']  # log-transformed Return_Amount
y_percentage = df['Return_Percentage']

# 4. Split the data into training and testing (70% train, 30% test)
X_train, X_test, y_train_amount, y_test_amount = train_test_split(X, y_amount, test_size=0.3, random_state=42)
_, _, y_train_percentage, y_test_percentage = train_test_split(X, y_percentage, test_size=0.3, random_state=42)

# 5. Train XGBoost models
# Model for predicting Return_Amount (Log-transformed)
xgb_model_amount = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=1000, learning_rate=0.05)
xgb_model_amount.fit(X_train, y_train_amount)

# Model for predicting Return_Percentage
xgb_model_percentage = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=1000, learning_rate=0.05)
xgb_model_percentage.fit(X_train, y_train_percentage)

# 6. Make predictions on the test set
y_pred_amount = xgb_model_amount.predict(X_test)
y_pred_percentage = xgb_model_percentage.predict(X_test)

# 7. Evaluate the models
# Return_Amount Model (Log-transformed)
r2_amount = r2_score(y_test_amount, y_pred_amount)
mse_amount = mean_squared_error(y_test_amount, y_pred_amount)
accuracy_amount = (1 - (mse_amount / np.var(y_test_amount))) * 100  # approximation of accuracy

# Return_Percentage Model
r2_percentage = r2_score(y_test_percentage, y_pred_percentage)
mse_percentage = mean_squared_error(y_test_percentage, y_pred_percentage)
accuracy_percentage = (1 - (mse_percentage / np.var(y_test_percentage))) * 100  # approximation of accuracy

print(f"✅ XGBoost Models trained successfully!\n")
print(f"📊 Return Amount Model - R² Score: {r2_amount:.4f}, MSE: {mse_amount:.2f}, Accuracy: {accuracy_amount:.2f}%")
print(f"📈 Return Percentage Model - R² Score: {r2_percentage:.4f}, MSE: {mse_percentage:.2f}, Accuracy: {accuracy_percentage:.2f}%")

# 8. Save the models for future use
joblib.dump(xgb_model_amount, 'xgb_return_amount_model.pkl')
joblib.dump(xgb_model_percentage, 'xgb_return_percentage_model.pkl')

print("💾 Models saved as 'xgb_return_amount_model.pkl' and 'xgb_return_percentage_model.pkl'")

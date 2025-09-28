import pandas as pd
from pathlib import Path

# Get the directory of the current script
base_dir = Path(__file__).resolve().parent.parent  # moves up from App/ to project root
# Construct file paths relative to the script
data_dir = base_dir / "DataSets" / "Datasets_Investment"
file_path_stocks = data_dir / "stocks.csv"
file_path_mutualFunds = data_dir / "mutualfunds.csv"
file_path_gold = data_dir / "gold.csv"
file_path_fd = data_dir / "fd.csv"

def calculateReturn(assetClass):
    path = ""
    if assetClass == "stocks":
        path = file_path_stocks
    elif assetClass == "mutualfunds":
        path = file_path_mutualFunds
    elif assetClass == "gold":
        path = file_path_gold
    else:
        path = file_path_fd
    # 1. Load the CSV file into a DataFrame
    df = pd.read_csv(path)
    # 2. Calculate the average of the 'PercentageOfReturn(%)' column
    average_return = df['PercentageOfReturn(%)'].mean()
    # 3. Print the result
    print(f"The average percentage of return is: {average_return:.2f}%")
    return round(average_return, 2)
if __name__ == "__main__":
    # Example usage
    print(calculateReturn("mutualfunds"))

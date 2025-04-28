import pandas as pd

file_path_stocks = r"C:\Users\DhanushAppireddy\Documents\GenAI_20-04-25\GenAIExpt\DataSets\Datasets_Investment\stocks.csv" 
file_path_mutualFunds = r"C:\Users\DhanushAppireddy\Documents\GenAI_20-04-25\GenAIExpt\DataSets\Datasets_Investment\mutualfunds.csv"
file_path_gold = r"C:\Users\DhanushAppireddy\Documents\GenAI_20-04-25\GenAIExpt\DataSets\Datasets_Investment\gold.csv"
file_path_fd = r"C:\Users\DhanushAppireddy\Documents\GenAI_20-04-25\GenAIExpt\DataSets\Datasets_Investment\fd.csv"

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

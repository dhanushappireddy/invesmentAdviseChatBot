import math

def calculate_tenure_years_months(initial_investment, expected_amount, annual_return_percent):
    # Convert percent to decimal
    r = annual_return_percent / 100
    
    if initial_investment <= 0 or expected_amount <= 0 or r <= 0:
        raise ValueError("All inputs must be greater than zero.")
    
    # Calculate total tenure in years (as a decimal)
    total_years = math.log(expected_amount / initial_investment) / math.log(1 + r)
    
    # Split into full years and remaining months
    years = int(total_years)
    months = round((total_years - years) * 12)

    return years, months
def calculate_expectedAmount(initial_investment, tenure, annual_return_percent):
    annual_return_rate = annual_return_percent / 100
    
    # Calculate compound interest
    expected_amount = initial_investment * (1 + annual_return_rate) ** tenure
    
    return int(expected_amount)

def calculate_tenure_years_months_String(initial_investment, expected_amount, annual_return_percent):
    # Convert percent to decimal
    r = annual_return_percent / 100
    
    if initial_investment <= 0 or expected_amount <= 0 or r <= 0:
        raise ValueError("All inputs must be greater than zero.")
    
    # Calculate total tenure in years (as a decimal)
    total_years = math.log(expected_amount / initial_investment) / math.log(1 + r)
    
    # Split into full years and remaining months
    years = int(total_years)
    months = round((total_years - years) * 12)
    print(f"Years: {years}")
    print(f"Months: {months}")
    return f"{years} years {months} months"

def calculate_percentage_return(invested_amount, return_amount):
    if invested_amount == 0:
        return 0  # Avoid division by zero
    percent = ((return_amount - invested_amount) / invested_amount) * 100
    return round(percent, 2)


if __name__ == "__main__":
    print("This is a.py")
    print(calculate_tenure_years_months(100000, 200000, 7))

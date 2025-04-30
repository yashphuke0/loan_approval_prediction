def calculate_emi(loan_amount, interest_rate, tenure_months):
    """
    Calculate monthly EMI (Equated Monthly Installment)

    Args:
        loan_amount (float): Loan amount in currency units
        interest_rate (float): Annual interest rate in percentage
        tenure_months (int): Loan tenure in months

    Returns:
        float: Monthly EMI amount
    """
    # Convert interest rate from % to decimal and make it monthly
    monthly_interest_rate = (interest_rate / 100) / 12

    # Calculate EMI using the formula: P * r * (1+r)^n / ((1+r)^n - 1)
    emi = loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** tenure_months / (
            ((1 + monthly_interest_rate) ** tenure_months) - 1)

    return emi


def perform_financial_checks(loan_amount, loan_term, applicant_income, coapplicant_income, existing_debt=0,
                             interest_rate=8.5):
    """
    Perform financial feasibility checks for loan approval

    Args:
        loan_amount (float): Loan amount in thousands
        loan_term (int): Loan term in months
        applicant_income (float): Monthly income of applicant
        coapplicant_income (float): Monthly income of co-applicant
        existing_debt (float): Existing monthly debt payments
        interest_rate (float): Annual loan interest rate in percentage

    Returns:
        dict: Dictionary containing financial check results
    """
    # Convert loan amount from thousands to actual amount
    loan_amount_actual = loan_amount

    total_income = applicant_income + coapplicant_income
    monthly_income = total_income

    # Calculate monthly EMI
    monthly_emi = calculate_emi(loan_amount_actual, interest_rate, loan_term)

    # Calculate loan to income ratio (monthly)
    loan_to_income_ratio = (monthly_emi / monthly_income) * 100 if monthly_income > 0 else float('inf')

    # Calculate debt to income ratio (monthly) - including the new loan EMI
    total_monthly_debt = monthly_emi + existing_debt
    debt_to_income_ratio =(total_monthly_debt / monthly_income) * 100 if monthly_income > 0 else float('inf')

    # Check if the applicant can afford the monthly EMI
    affordable = monthly_emi <= (monthly_income * 0.5)  # Rule of thumb: EMI should not exceed 50% of income

    # Check if ratios are within acceptable limits
    loan_to_income_ok = loan_to_income_ratio <= 40
    debt_to_income_ok = debt_to_income_ratio <= 43

    return {
        "monthly_emi": monthly_emi,
        "loan_to_income_ratio": loan_to_income_ratio,
        "debt_to_income_ratio": debt_to_income_ratio,
        "loan_to_income_ok": loan_to_income_ok,
        "debt_to_income_ok": debt_to_income_ok,
        "affordable": affordable,
        "financially_feasible": loan_to_income_ok and debt_to_income_ok and affordable
    }


def calculate_affordable_loan(monthly_income, interest_rate, tenure_months, max_emi_percent=0.3):
    """
    Calculate affordable loan amount based on income

    Args:
        monthly_income (float): Total monthly income
        interest_rate (float): Annual interest rate in percentage
        tenure_months (int): Loan tenure in months
        max_emi_percent (float): Maximum percentage of income for EMI

    Returns:
        float: Affordable loan amount
    """
    max_emi = monthly_income * max_emi_percent

    # Monthly interest rate
    monthly_rate = (interest_rate / 100) / 12

    # Calculate loan amount using EMI formula (rearranged)
    loan_amount = max_emi * ((1 - (1 + monthly_rate) ** (-tenure_months)) / monthly_rate)

    return loan_amount

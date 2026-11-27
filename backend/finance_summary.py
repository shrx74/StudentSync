from decimal import Decimal


def summarize(incomes, expenses):

    total_income = Decimal("0")
    total_expenses = Decimal("0")

    # Calculate total income
    for income in incomes:
        total_income += Decimal(str(income["amount"]))

    # Calculate total expenses
    for expense in expenses:
        total_expenses += Decimal(str(expense["amount"]))

    # Calculate remaining balance
    balance = total_income - total_expenses

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": balance
    }

def savings_progress(target_amount, contributions):

    target_amount = Decimal(str(target_amount))

    # Check if the target amount is valid
    if target_amount <= 0:
        raise ValueError("Target amount must be greater than zero")

    total_saved = Decimal("0")

    # Calculate total savings
    for contribution in contributions:
        total_saved += Decimal(str(contribution["amount"]))

    # Calculate savings percentage
    percent = round((total_saved / target_amount) * 100)

    # Limit progress to 100 percent
    percent = min(percent, 100)

    return {
        "total_saved": total_saved,
        "percent": percent
    }

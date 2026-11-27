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

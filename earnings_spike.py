from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

# Work out how many hours of a shift are paid
def paid_hours(start, end, unpaid_break):
    total_minutes = (end - start).total_seconds() / 60
    paid_minutes = total_minutes - unpaid_break
    return paid_minutes / 60


start = datetime(2026, 9, 18, 13, 0)
end = datetime(2026, 9, 18, 17, 30)
print("Paid hours:", paid_hours(start, end, 30))

def earnings_float(hours, wage):
    return hours * wage

# Earnings using Decimal
def earnings_decimal(hours, wage):
    result = Decimal(str(hours)) * Decimal(wage)
    return result.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

#Test: Float vs Decimal comparison
print("Float earnings:  ", earnings_float(3.5, 15.30))
print("Decimal earnings:", earnings_decimal(3.5, "15.30"))

# Test: overnight shift, 10:00 PM to 2:00 AM, no break
start = datetime(2026, 9, 18, 22, 0)
end = datetime(2026, 9, 19, 2, 0)
hours = paid_hours(start, end, 0)
print("Overnight paid hours:", hours)
print("Overnight earnings:", earnings_decimal(hours, "15.30"))
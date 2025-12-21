# src/Parameters/buy_vs_rent.py

def buying_case(
    property_price,
    down_payment,
    loan_rate,
    tax_rate,
    appreciation_rate,
    tenure_years=20
):
    loan_amount = property_price - down_payment
    r = loan_rate / 100 / 12
    n = tenure_years * 12

    emi = (loan_amount * r * (1 + r) ** n) / ((1 + r) ** n - 1)
    total_paid = emi * n
    interest_paid = total_paid - loan_amount

    future_value = property_price * ((1 + appreciation_rate / 100) ** tenure_years)
    tax_on_gain = (future_value - property_price) * (tax_rate / 100)

    wealth_buying = future_value - tax_on_gain - total_paid - down_payment

    return {
        "emi": round(emi, 2),
        "interest_paid": round(interest_paid, 2),
        "future_property_value": round(future_value, 2),
        "wealth_buying": round(wealth_buying, 2)
    }


def renting_case(
    initial_rent,
    escalation,
    down_payment,
    invest_rate,
    monthly_saving,
    tenure_years=20
):
    months = tenure_years * 12
    annual_rate = invest_rate / 100
    monthly_rate = annual_rate / 12

    total_rent_paid = 0
    current_rent = initial_rent

    for _ in range(tenure_years):
        total_rent_paid += current_rent * 12
        current_rent *= (1 + escalation / 100)

    lump_sum_value = down_payment * ((1 + annual_rate) ** tenure_years)

    sip_value = monthly_saving * (
        ((1 + monthly_rate) ** months - 1) / monthly_rate
    ) * (1 + monthly_rate)

    wealth_renting = lump_sum_value + sip_value - total_rent_paid

    return {
        "total_rent_paid": round(total_rent_paid, 2),
        "lump_sum_value": round(lump_sum_value, 2),
        "sip_value": round(sip_value, 2),
        "wealth_renting": round(wealth_renting, 2)
    }


def compare_results(buy, rent):
    if buy["wealth_buying"] > rent["wealth_renting"]:
        return "BUYING is financially better"
    elif rent["wealth_renting"] > buy["wealth_buying"]:
        return "RENTING is financially better"
    else:
        return "Both options are similar"

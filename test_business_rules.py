from customer_card import CustomerCard


def evaluate_application(customer: CustomerCard) -> dict:
    """
    Evaluate a validated application against business rules.

    IMPORTANT:
    This is currently a placeholder decision layer.
    Real lending rules should be provided by the lender.
    """

    # ---------------------------------------------------------
    # Safety check
    # ---------------------------------------------------------

    if customer.car_value is None:
        return {
            "status": "cannot_evaluate",
            "reason": "car_value_missing"
        }

    if customer.loan_amount is None:
        return {
            "status": "cannot_evaluate",
            "reason": "loan_amount_missing"
        }

    # ---------------------------------------------------------
    # Calculate requested loan-to-value ratio
    # ---------------------------------------------------------

    loan_to_value = (
        customer.loan_amount / customer.car_value
    )

    # ---------------------------------------------------------
    # No approval decision yet
    # ---------------------------------------------------------

    return {
        "status": "ready_for_business_decision",
        "loan_to_value": round(loan_to_value, 4),
        "loan_to_value_percent": round(
            loan_to_value * 100,
            2
        )
    }
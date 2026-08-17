from customer_card import CustomerCard


SUPPORTED_PROGRAMS = {
    "Автозалог",
    "Автозайм",
}


def validate_application(customer: CustomerCard) -> dict:
    """
    Validate a completed customer application.

    This function does NOT approve or reject a loan.
    It only checks whether the application data is valid.
    """

    errors = []

    # ---------------------------------------------------------
    # Vehicle validation
    # ---------------------------------------------------------

    if not customer.car_model:
        errors.append("car_model_missing")

    if customer.car_year is None:
        errors.append("car_year_missing")

    elif customer.car_year < 1900:
        errors.append("invalid_car_year")

    if customer.car_value is None:
        errors.append("car_value_missing")

    elif customer.car_value <= 0:
        errors.append("invalid_car_value")

    # ---------------------------------------------------------
    # Loan validation
    # ---------------------------------------------------------

    if customer.loan_amount is None:
        errors.append("loan_amount_missing")

    elif customer.loan_amount <= 0:
        errors.append("invalid_loan_amount")

    # ---------------------------------------------------------
    # Loan amount vs vehicle value
    # ---------------------------------------------------------

    if (
        customer.loan_amount is not None
        and customer.car_value is not None
        and customer.loan_amount > customer.car_value
    ):
        errors.append("loan_amount_exceeds_car_value")

    # ---------------------------------------------------------
    # Loan program
    # ---------------------------------------------------------

    if not customer.loan_program:
        errors.append("loan_program_missing")

    elif customer.loan_program not in SUPPORTED_PROGRAMS:
        errors.append("unsupported_loan_program")

    # ---------------------------------------------------------
    # Registration region
    # ---------------------------------------------------------

    if not customer.registration_region:
        errors.append("registration_region_missing")

    # ---------------------------------------------------------
    # Final result
    # ---------------------------------------------------------

    if errors:

        return {
            "valid": False,
            "errors": errors
        }

    return {
        "valid": True,
        "errors": []
    }
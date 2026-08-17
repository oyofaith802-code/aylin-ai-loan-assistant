from customer_card import CustomerCard


def get_missing_information(
    customer: CustomerCard
) -> list[str]:

    missing = []

    # --------------------------------------------------------
    # Vehicle
    # --------------------------------------------------------

    if not customer.car_model:
        missing.append("car_model")

    if customer.car_year is None:
        missing.append("car_year")

    if customer.car_value is None:
        missing.append("car_value")

    # --------------------------------------------------------
    # Loan
    # --------------------------------------------------------

    if customer.loan_amount is None:
        missing.append("loan_amount")

    if not customer.loan_program:
        missing.append("loan_program")

    if not customer.vehicle_possession:
        missing.append("vehicle_possession")

    # --------------------------------------------------------
    # Customer
    # --------------------------------------------------------

    if not customer.registration_region:
        missing.append("registration_region")

    # --------------------------------------------------------
    # Loan term
    # --------------------------------------------------------

    if customer.loan_term_months is None:
        missing.append("loan_term_months")

    return missing

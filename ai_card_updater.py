from customer_card import CustomerCard
from ai_extractor import extract_information_with_ai


# ============================================================
# UPDATE CUSTOMER CARD
# ============================================================

def update_customer_card_from_message(
    customer: CustomerCard,
    message: str
) -> dict:
    """
    Extract information from the latest customer message
    and merge only newly detected values into the customer card.

    IMPORTANT:
    None values from the extractor must NOT erase existing
    customer information.
    """

    extracted = extract_information_with_ai(
        message
    )

    # --------------------------------------------------------
    # CAR MODEL
    # --------------------------------------------------------

    if extracted.get("car_model") is not None:

        customer.car_model = (
            extracted["car_model"]
        )

    # --------------------------------------------------------
    # CAR YEAR
    # --------------------------------------------------------

    if extracted.get("car_year") is not None:

        customer.car_year = (
            extracted["car_year"]
        )

    # --------------------------------------------------------
    # CAR VALUE
    # --------------------------------------------------------

    if extracted.get("car_value") is not None:

        customer.car_value = (
            extracted["car_value"]
        )

    # --------------------------------------------------------
    # LOAN AMOUNT
    # --------------------------------------------------------

    if extracted.get("loan_amount") is not None:

        customer.loan_amount = (
            extracted["loan_amount"]
        )

    # --------------------------------------------------------
    # LOAN PROGRAM
    # --------------------------------------------------------

    if extracted.get("loan_program") is not None:

        customer.loan_program = (
            extracted["loan_program"]
        )

    # --------------------------------------------------------
    # VEHICLE POSSESSION
    # --------------------------------------------------------

    if extracted.get("vehicle_possession") is not None:

        customer.vehicle_possession = (
            extracted["vehicle_possession"]
        )

    # --------------------------------------------------------
    # REGISTRATION REGION
    # --------------------------------------------------------

    if extracted.get("registration_region") is not None:

        customer.registration_region = (
            extracted["registration_region"]
        )

    # --------------------------------------------------------
    # LOAN TERM
    # --------------------------------------------------------

    if extracted.get("loan_term_months") is not None:

        customer.loan_term_months = (
            extracted["loan_term_months"]
        )

    return extracted
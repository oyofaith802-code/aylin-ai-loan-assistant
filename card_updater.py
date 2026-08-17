from customer_card import CustomerCard


def update_customer_card(
    customer: CustomerCard,
    information: dict
) -> CustomerCard:
    """
    Update the customer card with newly extracted information.

    New information replaces old information.
    """

    if "car_model" in information:
        customer.car_model = information["car_model"]

    if "car_year" in information:
        customer.car_year = information["car_year"]

    if "car_value" in information:
        customer.car_value = information["car_value"]

    if "loan_amount" in information:
        customer.loan_amount = information["loan_amount"]

    if "loan_program" in information:
        customer.loan_program = information["loan_program"]

    if "registration_region" in information:
        customer.registration_region = information["registration_region"]

    return customer
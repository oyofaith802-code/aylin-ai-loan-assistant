from customer_card import CustomerCard
from ai_card_updater import update_customer_card_from_message


def test_ai_card_updater_extracts_and_updates_customer_card():

    customer = CustomerCard(
        application_id="APP-001",
        phone="test_phone"
    )

    message = (
        "У меня Toyota Camry 2021 года, "
        "хочу получить 500000 сом."
    )

    information = update_customer_card_from_message(
        customer,
        message
    )

    # Extracted information
    assert information["car_model"] == "Toyota Camry"
    assert information["car_year"] == 2021
    assert information["loan_amount"] == 500000.0

    # Information merged into CustomerCard
    assert customer.car_model == "Toyota Camry"
    assert customer.car_year == 2021
    assert customer.loan_amount == 500000.0

    # These weren't provided and must remain empty
    assert customer.car_value is None
    assert customer.loan_program is None
    assert customer.registration_region is None

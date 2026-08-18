from customer_card import CustomerCard
from ai_card_updater import update_customer_card_from_message


def test_ai_card_pipeline_updates_customer_card():

    customer = CustomerCard(
        application_id="TEST-001",
        phone="test_phone"
    )

    message = (
        "У меня Toyota Camry 2021 года, "
        "хочу получить 500000 сом."
    )

    result = update_customer_card_from_message(
        customer,
        message
    )

    # --------------------------------------------------------
    # Extracted information
    # --------------------------------------------------------

    assert result["car_model"] == "Toyota Camry"
    assert result["car_year"] == 2021
    assert result["loan_amount"] == 500000.0

    # --------------------------------------------------------
    # CustomerCard was updated
    # --------------------------------------------------------

    assert customer.car_model == "Toyota Camry"
    assert customer.car_year == 2021
    assert customer.loan_amount == 500000.0

    # --------------------------------------------------------
    # Information not present in the message
    # must remain empty
    # --------------------------------------------------------

    assert customer.car_value is None
    assert customer.loan_program is None
    assert customer.vehicle_possession is None
    assert customer.registration_region is None
    assert customer.loan_term_months is None

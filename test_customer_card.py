from customer_card import CustomerCard


def main():

    print("=" * 60)
    print("CUSTOMER CARD TEST")
    print("=" * 60)

    # --------------------------------------------------------
    # CREATE CUSTOMER
    # --------------------------------------------------------

    customer = CustomerCard(
        application_id="TEST-001",
        phone="+996700000000",
    )

    print("\nInitial customer:")
    print(customer.to_dict())

    print("\nCurrent stage:", customer.stage)

    assert customer.stage == "new"

    # --------------------------------------------------------
    # UPDATE CUSTOMER
    # --------------------------------------------------------

    customer.update({
        "car_model": "Toyota Camry",
        "car_year": 2021,
        "car_value": 1500000,
        "loan_amount": 500000,
        "loan_program": "Автозалог",
        "loan_term_months": 12,
        "vehicle_possession": "customer",
        "registration_region": "Бишкек",
    })

    print("\nUpdated customer:")
    print(customer.to_dict())

    # --------------------------------------------------------
    # VERIFY DATA
    # --------------------------------------------------------

    assert customer.car_model == "Toyota Camry"
    assert customer.car_year == 2021
    assert customer.car_value == 1500000
    assert customer.loan_amount == 500000
    assert customer.loan_program == "Автозалог"
    assert customer.loan_term_months == 12
    assert customer.vehicle_possession == "customer"
    assert customer.registration_region == "Бишкек"

    print("\nCustomer fields: PASS")

    # --------------------------------------------------------
    # UPDATE STAGE
    # --------------------------------------------------------

    customer.stage = "collecting_information"

    print(
        "\nCurrent stage after update:",
        customer.stage,
    )

    assert customer.stage == "collecting_information"

    print("Stage: PASS")

    # --------------------------------------------------------
    # TO DICT
    # --------------------------------------------------------

    data = customer.to_dict()

    assert data["application_id"] == "TEST-001"
    assert data["phone"] == "+996700000000"
    assert data["car_model"] == "Toyota Camry"
    assert data["car_year"] == 2021
    assert data["car_value"] == 1500000
    assert data["loan_amount"] == 500000
    assert data["loan_program"] == "Автозалог"
    assert data["loan_term_months"] == 12
    assert data["vehicle_possession"] == "customer"
    assert data["registration_region"] == "Бишкек"
    assert data["stage"] == "collecting_information"

    print("to_dict(): PASS")

    # --------------------------------------------------------
    # FROM DICT
    # --------------------------------------------------------

    restored = CustomerCard.from_dict(data)

    print("\nRestored customer:")
    print(restored.to_dict())

    assert restored.application_id == "TEST-001"
    assert restored.phone == "+996700000000"
    assert restored.car_model == "Toyota Camry"
    assert restored.car_year == 2021
    assert restored.car_value == 1500000
    assert restored.loan_amount == 500000
    assert restored.loan_program == "Автозалог"
    assert restored.loan_term_months == 12
    assert restored.vehicle_possession == "customer"
    assert restored.registration_region == "Бишкек"
    assert restored.stage == "collecting_information"

    print("from_dict(): PASS")

    # --------------------------------------------------------
    # FINAL
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("ALL CUSTOMER CARD CHECKS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
from customer_card import CustomerCard
from conversation_engine import process_customer_message


print("=" * 60)
print("AYLIN FULL CONVERSATION TEST")
print("=" * 60)


# =========================================================
# CUSTOMER
# =========================================================

customer = CustomerCard(
    application_id="TEST-FULL-001",
    phone="+996700000000"
)


# =========================================================
# TEST CONVERSATION
# =========================================================

messages = [
    "У меня Toyota Camry 2021 года, хочу получить 500000 сом.",
    "Примерная стоимость автомобиля 1500000 сом.",
    "Хочу автозалог.",
    "Без передачи автомобиля.",
    "Я зарегистрирован в Бишкеке.",
    "На 12 месяцев.",
]


# =========================================================
# PROCESS CONVERSATION
# =========================================================

for message in messages:

    print()
    print("=" * 60)

    print("CUSTOMER:")
    print(message)

    result = process_customer_message(
        customer,
        message
    )

    print()
    print("AYLIN:")
    print(result.get("response"))

    print()
    print("STATUS:", result.get("status"))
    print("NEXT FIELD:", result.get("next_field"))
    print("STAGE:", result.get("stage"))

    print()
    print("CUSTOMER CARD:")

    print(
        "Car model:",
        getattr(customer, "car_model", None)
    )

    print(
        "Car year:",
        getattr(customer, "car_year", None)
    )

    print(
        "Car value:",
        getattr(customer, "car_value", None)
    )

    print(
        "Loan amount:",
        getattr(customer, "loan_amount", None)
    )

    print(
        "Loan program:",
        getattr(customer, "loan_program", None)
    )

    print(
        "Vehicle possession:",
        getattr(customer, "vehicle_possession", None)
    )

    print(
        "Registration region:",
        getattr(customer, "registration_region", None)
    )

    print(
        "Loan term:",
        getattr(customer, "loan_term_months", None)
    )


# =========================================================
# FINISHED
# =========================================================

print()
print("=" * 60)
print("FULL CONVERSATION TEST FINISHED")
print("=" * 60)
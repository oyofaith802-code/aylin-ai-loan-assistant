from persistent_conversation import (
    process_persistent_message
)

from application_repository import (
    get_applications_by_phone
)


PHONE = "+996000000333"


# ============================================================
# APPLICATION 1
# ============================================================

print("=" * 60)
print("APPLICATION 1")
print("=" * 60)

messages_1 = [
    "У меня Toyota Camry 2021 года, хочу получить 500000 сом.",
    "Хочу автозалог.",
    "Я зарегистрирован в Бишкеке.",
    "Машина стоит примерно 1200000 сом."
]

for message in messages_1:

    result = process_persistent_message(
        phone=PHONE,
        message=message
    )

    print("\nCustomer:")
    print(message)

    print("\nAylin:")
    print(result["response"])

    print("Stage:", result.get("stage"))


# ============================================================
# APPLICATION 2
# ============================================================

print("\n" + "=" * 60)
print("APPLICATION 2")
print("=" * 60)

messages_2 = [
    "Хочу оформить новый автозалог.",
    "У меня Hyundai Sonata 2020 года.",
    "Хочу получить 400000 сом.",
    "Машина стоит примерно 1000000 сом.",
    "Я зарегистрирован в Бишкеке."
]

for message in messages_2:

    result = process_persistent_message(
        phone=PHONE,
        message=message
    )

    print("\nCustomer:")
    print(message)

    print("\nAylin:")
    print(result["response"])

    print("Stage:", result.get("stage"))


# ============================================================
# SHOW ALL APPLICATIONS
# ============================================================

print("\n" + "=" * 60)
print("ALL APPLICATIONS FOR CUSTOMER")
print("=" * 60)


applications = get_applications_by_phone(
    PHONE
)


for application in applications:

    print("\n" + "-" * 50)

    print(
        "Application ID:",
        application.application_id
    )

    print(
        "Car:",
        application.car_model
    )

    print(
        "Year:",
        application.car_year
    )

    print(
        "Car value:",
        application.car_value
    )

    print(
        "Loan amount:",
        application.loan_amount
    )

    print(
        "Program:",
        application.loan_program
    )

    print(
        "Region:",
        application.registration_region
    )

    print(
        "Stage:",
        application.stage
    )

    print(
        "Decision:",
        application.decision
    )

    print(
        "Reason:",
        application.decision_reason
    )


print("\n" + "=" * 60)
print("MULTIPLE APPLICATION TEST COMPLETE")
print("=" * 60)
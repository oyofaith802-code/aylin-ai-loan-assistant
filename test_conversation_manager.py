from conversation_manager import handle_customer_message

from application_manager import (
    get_customer_application_history,
)


PHONE = "+996000000555"


messages = [
    "У меня Toyota Camry 2021 года, хочу получить 500000 сом.",
    "Хочу автозалог.",
    "Я зарегистрирован в Бишкеке.",
    "Машина стоит примерно 1200000 сом.",
]


print("=" * 60)
print("REAL CONVERSATION MANAGER TEST")
print("=" * 60)


for message in messages:

    print("\n" + "=" * 60)

    print("Customer:")
    print(message)

    result = handle_customer_message(
        PHONE,
        message
    )

    print("\nAylin:")
    print(result["response"])

    print("\nApplication ID:")
    print(result["application_id"])

    print("\nStatus:")
    print(result["status"])

    print("\nStage:")
    print(result["stage"])


# ============================================================
# APPLICATION HISTORY
# ============================================================

print("\n")
print("=" * 60)
print("APPLICATION HISTORY")
print("=" * 60)

history = get_customer_application_history(
    PHONE
)

for application in history:

    print("\n------------------------------")

    print(
        "Application ID:",
        application["application_id"]
    )

    print(
        "Car:",
        application["car_model"]
    )

    print(
        "Year:",
        application["car_year"]
    )

    print(
        "Car value:",
        application["car_value"]
    )

    print(
        "Loan:",
        application["loan_amount"]
    )

    print(
        "Program:",
        application["loan_program"]
    )

    print(
        "Region:",
        application["registration_region"]
    )

    print(
        "Stage:",
        application["stage"]
    )

    print(
        "Decision:",
        application["decision"]
    )

    print(
        "Reason:",
        application["decision_reason"]
    )


print("\n")
print("=" * 60)
print("TEST COMPLETE")
print("=" * 60)
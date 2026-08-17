from application_status import (
    get_application_status,
    get_application_history
)

from application_status_response import (
    generate_status_response
)

from status_detector import (
    is_status_question
)


PHONE = "+996000000333"


print("=" * 60)
print("APPLICATION STATUS TEST")
print("=" * 60)


# ============================================================
# STATUS QUESTIONS
# ============================================================

messages = [
    "Какой статус моей заявки?",
    "Что с моей заявкой?",
    "Одобрена ли моя заявка?",
    "Как моя заявка?"
]


for message in messages:

    print("\nCustomer:")
    print(message)

    detected = is_status_question(
        message
    )

    print(
        "Status question:",
        detected
    )


# ============================================================
# CURRENT STATUS
# ============================================================

print("\n" + "=" * 60)
print("CURRENT APPLICATION STATUS")
print("=" * 60)


status = get_application_status(
    PHONE
)


print(status)


response = generate_status_response(
    status
)


print("\nAylin:")
print(response)


# ============================================================
# APPLICATION HISTORY
# ============================================================

print("\n" + "=" * 60)
print("APPLICATION HISTORY")
print("=" * 60)


history = get_application_history(
    PHONE
)


for application in history:

    print("\nApplication:")
    print(
        "ID:",
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
        "Loan:",
        application["loan_amount"]
    )

    print(
        "Stage:",
        application["stage"]
    )

    print(
        "Decision:",
        application["decision"]
    )


print("\n" + "=" * 60)
print("STATUS TEST COMPLETE")
print("=" * 60)
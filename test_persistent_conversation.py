from persistent_conversation import (
    process_persistent_message
)

from application_repository import (
    get_application_by_phone
)
PHONE = "+996000000222"
APPLICATION_ID = "TEST-PERSISTENT-003"





messages = [
    "У меня Toyota Camry 2021 года, хочу получить 500000 сом.",
    "Хочу автозалог.",
    "Я зарегистрирован в Бишкеке.",
    "Машина стоит примерно 1200000 сом."
]


print("=" * 60)
print("PERSISTENT AYLIN CONVERSATION TEST")
print("=" * 60)


for message in messages:

    print("\n" + "=" * 60)

    print("Customer:")
    print(message)

    result = process_persistent_message(
        phone=PHONE,
        message=message,
        application_id=APPLICATION_ID
    )

    print("\nAylin:")
    print(result["response"])

    print("\nStatus:")
    print(result["status"])

    print("\nStage:")
    print(result.get("stage"))


# ------------------------------------------------------------
# Load from database after conversation
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("DATABASE STATE AFTER CONVERSATION")
print("=" * 60)


application = get_application_by_phone(
    PHONE
)

print(
    "Application ID:",
    application.application_id
)

print(
    "Phone:",
    application.phone
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
    "Loan program:",
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
    "Decision reason:",
    application.decision_reason
)


print("\n" + "=" * 60)
print("PERSISTENT CONVERSATION TEST COMPLETE")
print("=" * 60)
from customer_card import CustomerCard

from application_repository import (
    create_application_table,
    save_customer,
    get_application,
    get_application_by_phone,
    save_decision
)


print("=" * 60)
print("APPLICATION REPOSITORY TEST")
print("=" * 60)


# ------------------------------------------------------------
# Create database table
# ------------------------------------------------------------

create_application_table()

print("\nDatabase table created.")


# ------------------------------------------------------------
# Create customer
# ------------------------------------------------------------

customer = CustomerCard(
    application_id="TEST-DB-001",
    phone="+996000000000",

    car_model="Toyota Camry",
    car_year=2021,
    car_value=1200000,

    loan_amount=500000,
    loan_program="Автозалог",

    registration_region="Бишкек",

    stage="collecting_information"
)


# ------------------------------------------------------------
# Save
# ------------------------------------------------------------

save_customer(customer)

print("\nApplication saved.")


# ------------------------------------------------------------
# Load by ID
# ------------------------------------------------------------

application = get_application(
    "TEST-DB-001"
)

print("\nLoaded application:")

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


# ------------------------------------------------------------
# Save decision
# ------------------------------------------------------------

save_decision(
    "TEST-DB-001",
    "approved",
    "lender_policy_passed"
)

print("\nDecision saved.")


# ------------------------------------------------------------
# Load again
# ------------------------------------------------------------

application = get_application(
    "TEST-DB-001"
)

print("\nFinal database record:")

print(
    "Decision:",
    application.decision
)

print(
    "Reason:",
    application.decision_reason
)


# ------------------------------------------------------------
# Find by phone
# ------------------------------------------------------------

application = get_application_by_phone(
    "+996000000000"
)

print("\nSearch by phone:")

print(
    "Found:",
    application.application_id
)

print(
    "Stage:",
    application.stage
)

print(
    "Decision:",
    application.decision
)

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
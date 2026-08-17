from customer_card import CustomerCard
from application_pipeline import run_application_pipeline


def print_result(title, customer):
    print("=" * 60)
    print(title)
    print("=" * 60)

    print("Before:")
    print("Stage:", customer.stage)

    result = run_application_pipeline(customer)

    print("\nResult:")
    print(result)

    print("\nAfter:")
    print("Stage:", customer.stage)

    print()


# =========================================================
# TEST 1 — APPROVED
# =========================================================

approved_customer = CustomerCard(
    application_id="TEST-APPROVED",
    phone="+996000000001",
    car_model="Toyota Camry",
    car_year=2021,
    car_value=1_200_000,
    loan_amount=500_000,
    loan_program="Автозалог",
    registration_region="Бишкек",
    stage="collecting_information"
)

print_result(
    "TEST 1 — APPROVED",
    approved_customer
)


# =========================================================
# TEST 2 — REJECTED: LTV TOO HIGH
# =========================================================

rejected_customer = CustomerCard(
    application_id="TEST-REJECTED",
    phone="+996000000002",
    car_model="Toyota Camry",
    car_year=2021,
    car_value=1_000_000,
    loan_amount=800_000,
    loan_program="Автозалог",
    registration_region="Бишкек",
    stage="collecting_information"
)

print_result(
    "TEST 2 — REJECTED",
    rejected_customer
)


# =========================================================
# TEST 3 — REJECTED: OLD VEHICLE
# =========================================================

old_car_customer = CustomerCard(
    application_id="TEST-OLD-CAR",
    phone="+996000000003",
    car_model="Toyota Camry",
    car_year=2005,
    car_value=1_000_000,
    loan_amount=500_000,
    loan_program="Автозалог",
    registration_region="Бишкек",
    stage="collecting_information"
)

print_result(
    "TEST 3 — OLD VEHICLE",
    old_car_customer
)
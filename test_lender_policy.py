from customer_card import CustomerCard
from lender_policy import evaluate_lender_policy


def create_customer(
    car_value=1_500_000,
    loan_amount=400_000,
    car_year=2024,
    loan_program="Автозалог",
):
    return CustomerCard(
        application_id="TEST-POLICY",
        phone="+996TEST",
        car_model="BYD Song Plus",
        car_year=car_year,
        car_value=car_value,
        loan_amount=loan_amount,
        loan_program=loan_program,
        vehicle_possession="customer",
        registration_region="Бишкеке",
        loan_term_months=1,
    )


def run_test(name, customer):
    result = evaluate_lender_policy(customer)

    print("=" * 60)
    print(name)
    print("=" * 60)
    print("Decision:", result.get("decision"))
    print("Eligible:", result.get("eligible"))
    print("Errors:", result.get("errors"))
    print(
        "LTV:",
        result.get("loan_to_value_percent")
    )
    print()


# ============================================================
# 1. VALID APPLICATION
# ============================================================

run_test(
    "TEST 1 — VALID APPLICATION",
    create_customer(
        car_value=1_500_000,
        loan_amount=400_000,
        car_year=2024,
    )
)


# ============================================================
# 2. LOAN BELOW MINIMUM
# ============================================================

run_test(
    "TEST 2 — LOAN BELOW MINIMUM",
    create_customer(
        car_value=1_500_000,
        loan_amount=40_000,
        car_year=2024,
    )
)


# ============================================================
# 3. LOAN ABOVE MAXIMUM
# ============================================================

run_test(
    "TEST 3 — LOAN ABOVE MAXIMUM",
    create_customer(
        car_value=10_000_000,
        loan_amount=6_000_000,
        car_year=2024,
    )
)


# ============================================================
# 4. OLD VEHICLE
# ============================================================

run_test(
    "TEST 4 — VEHICLE TOO OLD",
    create_customer(
        car_value=1_000_000,
        loan_amount=400_000,
        car_year=2009,
    )
)


# ============================================================
# 5. LTV TOO HIGH
# ============================================================

run_test(
    "TEST 5 — LTV ABOVE 70%",
    create_customer(
        car_value=500_000,
        loan_amount=400_000,
        car_year=2024,
    )
)


# ============================================================
# 6. UNSUPPORTED PROGRAM
# ============================================================

run_test(
    "TEST 6 — UNSUPPORTED LOAN PROGRAM",
    create_customer(
        car_value=1_500_000,
        loan_amount=400_000,
        car_year=2024,
        loan_program="Другой займ",
    )
)


# ============================================================
# 7. MISSING CAR VALUE
# ============================================================

customer = create_customer(
    car_value=None,
    loan_amount=400_000,
)

run_test(
    "TEST 7 — MISSING CAR VALUE",
    customer
)


# ============================================================
# 8. MISSING LOAN AMOUNT
# ============================================================

customer = create_customer(
    car_value=1_500_000,
    loan_amount=None,
)

run_test(
    "TEST 8 — MISSING LOAN AMOUNT",
    customer
)


print("=" * 60)
print("ALL POLICY TESTS COMPLETE")
print("=" * 60)
from customer_card import CustomerCard
from decision_response import generate_decision_response


customer = CustomerCard(
    application_id="TEST-001",
    phone="+996000000000",
    car_model="Toyota Camry",
    car_year=2021,
    car_value=1_200_000,
    loan_amount=500_000,
    loan_program="Автозалог",
    registration_region="Бишкек",
    stage="business_decision"
)


# =========================================================
# TEST 1 — APPROVED
# =========================================================

print("=" * 60)
print("TEST 1 — APPROVED")
print("=" * 60)

approved_decision = {
    "decision": "approved",
    "reason": "lender_policy_passed",
    "loan_to_value": 0.4167,
    "loan_to_value_percent": 41.67
}

print(
    generate_decision_response(
        approved_decision,
        customer
    )
)


# =========================================================
# TEST 2 — REJECTED: LTV
# =========================================================

print("\n" + "=" * 60)
print("TEST 2 — REJECTED: LTV TOO HIGH")
print("=" * 60)

rejected_ltv = {
    "decision": "rejected",
    "reason": "lender_policy_failed",
    "errors": [
        "loan_to_value_exceeds_limit"
    ],
    "loan_to_value": 0.8,
    "loan_to_value_percent": 80.0
}

print(
    generate_decision_response(
        rejected_ltv,
        customer
    )
)


# =========================================================
# TEST 3 — REJECTED: OLD VEHICLE
# =========================================================

print("\n" + "=" * 60)
print("TEST 3 — VEHICLE TOO OLD")
print("=" * 60)

rejected_old_car = {
    "decision": "rejected",
    "reason": "lender_policy_failed",
    "errors": [
        "vehicle_too_old"
    ],
    "loan_to_value": 0.5,
    "loan_to_value_percent": 50.0
}

print(
    generate_decision_response(
        rejected_old_car,
        customer
    )
)


# =========================================================
# TEST 4 — MANUAL REVIEW
# =========================================================

print("\n" + "=" * 60)
print("TEST 4 — MANUAL REVIEW")
print("=" * 60)

manual_review = {
    "decision": "manual_review",
    "reason": "lender_policy_required"
}

print(
    generate_decision_response(
        manual_review,
        customer
    )
)
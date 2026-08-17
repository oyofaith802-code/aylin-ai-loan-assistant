from customer_card import CustomerCard
from application_validator import validate_application


# ============================================================
# TEST 1 — VALID APPLICATION
# ============================================================

customer = CustomerCard(
    application_id="TEST-001",
    phone="+996000000000"
)

customer.car_model = "Toyota Camry"
customer.car_year = 2021
customer.car_value = 1200000.0

customer.loan_amount = 500000.0
customer.loan_program = "Автозалог"

customer.registration_region = "Бишкек"


print("=" * 60)
print("TEST 1 — VALID APPLICATION")
print("=" * 60)

result = validate_application(customer)

print(result)


# ============================================================
# TEST 2 — LOAN GREATER THAN CAR VALUE
# ============================================================

customer.loan_amount = 1500000.0


print("\n" + "=" * 60)
print("TEST 2 — LOAN EXCEEDS CAR VALUE")
print("=" * 60)

result = validate_application(customer)

print(result)


# ============================================================
# TEST 3 — MISSING INFORMATION
# ============================================================

customer.loan_amount = 500000.0
customer.car_value = None


print("\n" + "=" * 60)
print("TEST 3 — MISSING CAR VALUE")
print("=" * 60)

result = validate_application(customer)

print(result)
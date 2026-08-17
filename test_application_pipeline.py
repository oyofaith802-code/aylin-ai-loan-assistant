from customer_card import CustomerCard

from application_pipeline import (
    run_application_pipeline
)


print("=" * 60)
print("FULL APPLICATION PIPELINE TEST")
print("=" * 60)


# =========================================================
# CREATE COMPLETE CUSTOMER APPLICATION
# Same data collected from full conversation test
# =========================================================

customer = CustomerCard(
    application_id="TEST-001",
    phone="+996000000000"
)


# =========================================================
# FILL CUSTOMER CARD
# =========================================================

customer.car_model = "Toyota Camry"
customer.car_year = 2021
customer.car_value = 1_500_000

customer.loan_amount = 500_000
customer.loan_program = "Автозалог"

customer.vehicle_possession = "customer"

customer.registration_region = "Бишкек"

customer.loan_term_months = 12


# =========================================================
# INITIAL STAGE
# =========================================================

print()
print("Before pipeline:")
print("Stage:", customer.stage)


# =========================================================
# RUN APPLICATION PIPELINE
# =========================================================

result = run_application_pipeline(
    customer
)


# =========================================================
# OUTPUT RESULT
# =========================================================

print()
print("Pipeline result:")
print(result)


# =========================================================
# CUSTOMER CARD AFTER PROCESSING
# =========================================================

print()
print("Customer Card:")
print("Car model:", customer.car_model)
print("Car year:", customer.car_year)
print("Car value:", customer.car_value)

print("Loan amount:", customer.loan_amount)
print("Loan program:", customer.loan_program)

print(
    "Vehicle possession:",
    customer.vehicle_possession
)

print(
    "Registration region:",
    customer.registration_region
)

print(
    "Loan term:",
    customer.loan_term_months
)


print()
print("After pipeline:")
print("Stage:", customer.stage)


print()
print("=" * 60)
print("APPLICATION PIPELINE TEST FINISHED")
print("=" * 60)
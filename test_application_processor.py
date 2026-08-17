from customer_card import CustomerCard
from application_processor import process_application


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

customer.stage = "processing_application"


result = process_application(customer)


print("=" * 60)
print("APPLICATION PROCESSOR TEST")
print("=" * 60)

print(result)
print("\n" + "=" * 60)
print("INVALID APPLICATION TEST")
print("=" * 60)

customer.loan_amount = 1500000.0

result = process_application(customer)

print(result)
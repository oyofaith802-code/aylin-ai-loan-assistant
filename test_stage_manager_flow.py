from customer_card import CustomerCard
from stage_manager import process_stage


customer = CustomerCard(
    application_id="APP-001",
    phone="test_phone",
    car_model="Camry",
    car_year=2021,
    car_value=1500000,
    loan_amount=500000,
    loan_program="Автозалог",
    registration_region="Бишкек"
)

print("Before:", customer.stage)

result = process_stage(customer)

print("Result:", result)
print("After:", customer.stage)
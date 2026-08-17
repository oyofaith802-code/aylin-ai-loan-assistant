from customer_card import CustomerCard
from stage_flow import process_information_stage


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

result = process_information_stage(customer)

print("Stage result:")
print(result)
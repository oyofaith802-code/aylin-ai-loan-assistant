from customer_card import CustomerCard
from next_question import get_next_required_information


customer = CustomerCard(
    application_id="APP-001",
    phone="test_phone",
    car_model="Camry",
    car_year=2021,
    car_value=1500000,
    loan_amount=500000
)

next_information = get_next_required_information(customer)

print("Next required information:")
print(next_information)
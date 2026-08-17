from customer_card import CustomerCard
from required_information import get_missing_information


customer = CustomerCard(
    application_id="APP-001",
    phone="test_phone",
    car_model="Camry",
    car_year=2021,
    car_value=1500000,
    loan_amount=500000
)

missing = get_missing_information(customer)

print("Missing information:")
for item in missing:
    print("-", item)
from customer_card import CustomerCard
from conversation_engine import process_customer_message


customer = CustomerCard(
    application_id="APP-001",
    phone="test_phone",
    car_model="Camry",
    car_year=2021,
    car_value=1500000,
    loan_amount=500000
)

message = "Здравствуйте, хочу оформить займ."

result = process_customer_message(
    customer,
    message
)

print("Customer:", message)
print("Aylin:", result)
from customer_card import CustomerCard
from ai_conversation import process_ai_message


customer = CustomerCard(
    application_id="APP-001",
    phone="test_phone"
)

message = (
    "У меня Toyota Camry 2021 года, "
    "хочу получить 500000 сом."
)

result = process_ai_message(
    customer,
    message
)

print("Customer:")
print(message)

print("\nAI extracted:")
print(result["extracted_information"])

print("\nAylin:")
print(result["conversation"])

print("\nCustomer card:")
print("Car model:", customer.car_model)
print("Car year:", customer.car_year)
print("Loan amount:", customer.loan_amount)
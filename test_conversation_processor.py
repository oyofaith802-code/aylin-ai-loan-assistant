from customer_card import CustomerCard
from conversation_processor import process_message


customer = CustomerCard(
    application_id="APP-001",
    phone="test_phone"
)

message = (
    "У меня Toyota Camry 2021 года, "
    "хочу получить 500000 сом."
)

result = process_message(
    customer,
    message
)

print("Extracted information:")
print(result["extracted_information"])

print("\nCustomer card:")
print("Car model:", customer.car_model)
print("Car year:", customer.car_year)
print("Loan amount:", customer.loan_amount)

print("\nAylin:")
print(result["conversation"])
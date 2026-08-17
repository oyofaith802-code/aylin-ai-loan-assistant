from customer_card import CustomerCard
from ai_card_updater import process_message_with_ai


customer = CustomerCard(
    application_id="APP-001",
    phone="test_phone"
)

message = "У меня Toyota Camry 2021 года, хочу получить 500000 сом."

information = process_message_with_ai(
    customer,
    message
)

print("AI extracted:")
print(information)

print("\nCustomer card after AI update:")
print("Car model:", customer.car_model)
print("Car year:", customer.car_year)
print("Car value:", customer.car_value)
print("Loan amount:", customer.loan_amount)
print("Loan program:", customer.loan_program)
print("Registration region:", customer.registration_region)
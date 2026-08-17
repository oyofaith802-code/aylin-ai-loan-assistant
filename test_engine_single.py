from customer_card import CustomerCard
from aylin_engine import process_customer_message


customer = CustomerCard(
    application_id="TEST-ENGINE",
    phone="test_phone"
)

message = "У меня Toyota Camry 2021 года, хочу получить 500000 сом."

print("Customer:")
print(message)

result = process_customer_message(
    customer,
    message
)

print("\nAylin result:")
print(result)

print("\nCustomer card:")
print("Car model:", customer.car_model)
print("Car year:", customer.car_year)
print("Car value:", customer.car_value)
print("Loan amount:", customer.loan_amount)
print("Loan program:", customer.loan_program)
print("Registration region:", customer.registration_region)
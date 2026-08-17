from customer_card import CustomerCard
from aylin_engine import process_customer_message


customer = CustomerCard(
    application_id="APP-001",
    phone="test_phone"
)


message = (
    "У меня Toyota Camry 2021 года, "
    "хочу получить 500000 сом."
)


result = process_customer_message(
    customer,
    message
)


print("Customer:")
print(message)

print("\nAylin result:")
print(result)

print("\nCustomer card:")
print("Car model:", customer.car_model)
print("Car year:", customer.car_year)
print("Loan amount:", customer.loan_amount)
print("Loan program:", customer.loan_program)
print("Registration region:", customer.registration_region)
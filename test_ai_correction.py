from customer_card import CustomerCard
from ai_conversation import process_ai_message


customer = CustomerCard(
    application_id="APP-001",
    phone="test_phone"
)


# ---------------------------------------------------------
# First message
# ---------------------------------------------------------

message_1 = (
    "У меня Toyota Camry 2021 года, "
    "хочу получить 500000 сом."
)

result_1 = process_ai_message(
    customer,
    message_1
)

print("After first message:")
print("Car model:", customer.car_model)
print("Car year:", customer.car_year)
print("Loan amount:", customer.loan_amount)


# ---------------------------------------------------------
# Customer corrects the year and loan amount
# ---------------------------------------------------------

message_2 = (
    "Нет, я ошибся. Машина 2022 года, "
    "хочу 700000 сом."
)

result_2 = process_ai_message(
    customer,
    message_2
)

print("\nAfter customer correction:")
print("Car model:", customer.car_model)
print("Car year:", customer.car_year)
print("Loan amount:", customer.loan_amount)
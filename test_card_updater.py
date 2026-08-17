from customer_card import CustomerCard
from message_extractor import extract_customer_information
from card_updater import update_customer_card


customer = CustomerCard(
    application_id="APP-001",
    phone="test_phone"
)

# ---------------------------------------------------------
# First customer message
# ---------------------------------------------------------

message_1 = (
    "У меня Toyota Camry 2021 года, "
    "хочу получить 500000 сом."
)

information_1 = extract_customer_information(message_1)

update_customer_card(customer, information_1)

print("After first message:")
print("Car model:", customer.car_model)
print("Car year:", customer.car_year)
print("Loan amount:", customer.loan_amount)


# ---------------------------------------------------------
# Customer changes the information
# ---------------------------------------------------------

message_2 = (
    "Нет, у меня Toyota Corolla 2022 года, "
    "хочу 700000 сом."
)

information_2 = extract_customer_information(message_2)

update_customer_card(customer, information_2)

print("\nAfter customer changed the information:")
print("Car model:", customer.car_model)
print("Car year:", customer.car_year)
print("Loan amount:", customer.loan_amount)
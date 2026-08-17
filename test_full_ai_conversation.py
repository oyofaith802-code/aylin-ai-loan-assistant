from customer_card import CustomerCard
from ai_conversation import process_ai_message


customer = CustomerCard(
    application_id="APP-001",
    phone="test_phone"
)


messages = [
    "У меня Toyota Camry 2021 года, хочу получить 500000 сом.",
    "Хочу автозалог.",
    "Я зарегистрирован в Бишкеке."
]


for message in messages:

    print("=" * 60)

    print("Customer:")
    print(message)

    result = process_ai_message(
        customer,
        message
    )

    print("\nAI extracted:")
    print(result["extracted_information"])

    print("\nAylin:")
    print(result["conversation"])

    print("\nCustomer card:")
    print("Car model:", customer.car_model)
    print("Car year:", customer.car_year)
    print("Loan amount:", customer.loan_amount)
    print("Loan program:", customer.loan_program)
    print("Registration region:", customer.registration_region)
from customer_card import CustomerCard
from conversation_application import process_conversation_message


customer = CustomerCard(
    application_id="TEST-001",
    phone="+996000000000"
)


messages = [
    "У меня Toyota Camry 2021 года, хочу получить 500000 сом.",
    "Хочу автозалог.",
    "Я зарегистрирован в Бишкеке.",
    "Машина стоит примерно 1200000 сом."
]


print("=" * 60)
print("FULL AYLIN → APPLICATION PIPELINE TEST")
print("=" * 60)


for message in messages:

    print("\n" + "=" * 60)
    print("Customer:")
    print(message)

    result = process_conversation_message(
        customer,
        message
    )

    print("\nAylin:")
    print(result)

    print("\nCustomer Card:")
    print(f"Car model: {customer.car_model}")
    print(f"Car year: {customer.car_year}")
    print(f"Car value: {customer.car_value}")
    print(f"Loan amount: {customer.loan_amount}")
    print(f"Loan program: {customer.loan_program}")
    print(f"Registration region: {customer.registration_region}")
    print(f"Stage: {customer.stage}")


print("\n" + "=" * 60)
print("FINAL RESULT")
print("=" * 60)

print("Car model:", customer.car_model)
print("Car year:", customer.car_year)
print("Car value:", customer.car_value)
print("Loan amount:", customer.loan_amount)
print("Loan program:", customer.loan_program)
print("Registration region:", customer.registration_region)
print("Stage:", customer.stage)
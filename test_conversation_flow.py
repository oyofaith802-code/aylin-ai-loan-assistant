from customer_card import CustomerCard
from aylin_engine import process_customer_message


def print_card(customer):
    print("Customer card:")
    print(f"Car model: {customer.car_model}")
    print(f"Car year: {customer.car_year}")
    print(f"Car value: {customer.car_value}")
    print(f"Loan amount: {customer.loan_amount}")
    print(f"Loan program: {customer.loan_program}")
    print(f"Registration region: {customer.registration_region}")
    print(f"Stage: {customer.stage}")


customer = CustomerCard(
    application_id="TEST-001",
    phone="+996000000000"
)

conversation_history = []


messages = [
    "У меня Toyota Camry 2021 года, хочу получить 500000 сом.",
    "Хочу автозалог.",
    "Я зарегистрирован в Бишкеке.",
    "Машина стоит примерно 1200000 сом."
]


for message in messages:

    print("=" * 60)

    print("Customer:")
    print(message)

    result = process_customer_message(
        customer,
        message,
        conversation_history
    )

    print("\nAylin:")
    print(result["response"])

    print("\nResult:")
    print(result)

    print()

    print_card(customer)

    # Save conversation history
    conversation_history.append({
        "role": "customer",
        "content": message
    })

    conversation_history.append({
        "role": "assistant",
        "content": result["response"]
    })


print("=" * 60)
print("FINAL CUSTOMER CARD")
print("=" * 60)

print_card(customer)
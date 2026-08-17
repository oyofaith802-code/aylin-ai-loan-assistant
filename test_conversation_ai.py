from conversation_ai import generate_ai_response


customer_message = (
    "У меня Toyota Camry 2021 года, "
    "хочу получить 500000 сом."
)

response = generate_ai_response(
    customer_message=customer_message,
    next_question="Какова примерная стоимость автомобиля?",
    conversation_history=[],
    customer_data={
        "car_model": "Toyota Camry",
        "car_year": 2021,
        "loan_amount": 500000
    }
)

print("Customer:")
print(customer_message)

print("\nAylin:")
print(response)
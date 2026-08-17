from message_extractor import extract_customer_information


messages = [
    "Я зарегистрирован в Бишкеке.",
    "Регистрация у меня в Оше.",
    "Я из Каракола."
]


for message in messages:
    information = extract_customer_information(message)

    print("Customer:", message)
    print("Extracted:", information)
    print()
from message_extractor import extract_customer_information


messages = [
    "Хочу автозалог.",
    "Мне нужен автозайм.",
    "Хочу взять займ под залог автомобиля."
]


for message in messages:
    information = extract_customer_information(message)

    print("Customer:", message)
    print("Extracted:", information)
    print()
from message_extractor import extract_customer_information


message = "У меня Toyota Camry 2021 года, хочу получить 500000 сом."

information = extract_customer_information(message)

print("Customer message:")
print(message)

print("\nExtracted information:")

for key, value in information.items():
    print(f"- {key}: {value}")
from ai_extractor import extract_information_with_ai


message = (
    "Машина стоит 1200000 сом, "
    "хочу получить 500000 сом."
)

result = extract_information_with_ai(message)

print("Customer:")
print(message)

print("\nAI extracted:")

for key, value in result.items():
    print(f"- {key}: {value}")
from conversation_memory import ConversationMemory
from ai_chat import chat_with_ai


memory = ConversationMemory()

memory.add_customer_message(
    "У меня Toyota Camry 2021 года."
)

memory.add_ai_message(
    "Какую сумму займа вы хотите получить?"
)

current_message = "Около 500000 сом."

response = chat_with_ai(
    memory,
    current_message
)

print("Customer:")
print(current_message)

print("\nAylin:")
print(response)
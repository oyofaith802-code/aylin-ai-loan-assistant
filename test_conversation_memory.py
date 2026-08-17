from conversation_memory import ConversationMemory


memory = ConversationMemory()

memory.add_customer_message(
    "У меня Toyota Camry 2021 года."
)

memory.add_ai_message(
    "Какую сумму займа вы хотите получить?"
)

memory.add_customer_message(
    "Около 500000 сом."
)

print("Conversation history:")

for message in memory.get_history():
    print(f"{message['role']}: {message['content']}")
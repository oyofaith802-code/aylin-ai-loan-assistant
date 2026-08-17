from conversation_memory import ConversationMemory
from ai_conversation_prompt import build_conversation_prompt


memory = ConversationMemory()

memory.add_customer_message(
    "У меня Toyota Camry 2021 года."
)

memory.add_ai_message(
    "Какую сумму займа вы хотите получить?"
)

current_message = "Около 500000 сом."

prompt = build_conversation_prompt(
    memory,
    current_message
)

print(prompt)
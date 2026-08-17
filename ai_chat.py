from conversation_memory import ConversationMemory
from ai_conversation_prompt import build_conversation_prompt
from llm import ask_ai


def chat_with_ai(
    memory: ConversationMemory,
    current_message: str
) -> str:
    """
    Send the conversation history and the current
    customer message to Ollama.
    """

    prompt = build_conversation_prompt(
        memory,
        current_message
    )

    response = ask_ai(prompt)

    return response.strip()
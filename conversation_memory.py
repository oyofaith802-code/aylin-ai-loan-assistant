from dataclasses import dataclass, field


@dataclass
class ConversationMessage:
    role: str
    content: str


@dataclass
class ConversationMemory:
    messages: list[ConversationMessage] = field(
        default_factory=list
    )

    def add_customer_message(self, message: str):
        self.messages.append(
            ConversationMessage(
                role="customer",
                content=message
            )
        )

    def add_ai_message(self, message: str):
        self.messages.append(
            ConversationMessage(
                role="assistant",
                content=message
            )
        )

    def get_history(self) -> list[dict]:
        return [
            {
                "role": message.role,
                "content": message.content
            }
            for message in self.messages
        ]
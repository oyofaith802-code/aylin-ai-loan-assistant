def is_status_question(message: str) -> bool:
    """
    Detect whether the customer is asking about
    the status of their application.
    """

    text = message.lower().strip()

    status_phrases = [
        "какой статус",
        "какой статус моей заявки",
        "статус заявки",
        "статус моей заявки",
        "что с моей заявкой",
        "что с заявкой",
        "одобрена ли моя заявка",
        "одобрили ли мою заявку",
        "моя заявка одобрена",
        "заявка одобрена",
        "решение по заявке",
        "есть решение",
        "что с кредитом",
        "как моя заявка"
    ]

    return any(
        phrase in text
        for phrase in status_phrases
    )
import requests


OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
OLLAMA_MODEL = "qwen2.5:3b"


SYSTEM_PROMPT = """
Ты — Айлин, AI-менеджер ломбарда «Молодой».

Твоя задача — ТОЛЬКО естественно сформулировать сообщение,
которое уже подготовила система.

КРИТИЧЕСКИЕ ПРАВИЛА:

1. Никогда не придумывай информацию.
2. Никогда не придумывай числа.
3. Никогда не придумывай цены.
4. Никогда не придумывай процентные ставки.
5. Никогда не придумывай сроки.
6. Никогда не придумывай условия займа.
7. Никогда не оценивай автомобиль.
8. Никогда не рассчитывай сумму займа.
9. Никогда не принимай решение по заявке.
10. Никогда не добавляй информацию от себя.
11. Если система дала готовый вопрос, нужно только естественно
    переформулировать этот вопрос.
12. Не отвечай на вопрос клиента, если система попросила задать вопрос.
13. Не добавляй объяснения.
14. Не добавляй примеры.
15. Не добавляй диапазоны цен.
16. Не добавляй валюту, если её нет в исходном сообщении системы.
17. Сохраняй смысл исходного сообщения системы.

Язык:

- Если клиент пишет на русском — отвечай на русском.
- Если клиент пишет на кыргызском — отвечай на кыргызском.

Ответ должен быть коротким: обычно одно предложение.
"""


def detect_language(text: str) -> str:
    """
    Detect the customer's language.

    Kyrgyz has several characters and common words that
    distinguish it from Russian.
    """

    text_lower = text.lower()

    kyrgyz_markers = [
        "ө",
        "ү",
        "ң",
        "қ",
        "ғ",
        "һ",
        "менин",
        "унаа",
        "унаам",
        "жылкы",
        "канча",
        "кредит",
        "зайым",
        "автоунаа",
        "катталган",
    ]

    for marker in kyrgyz_markers:
        if marker in text_lower:
            return "kyrgyz"

    return "russian"


def generate_ai_response(
    customer_message: str,
    next_question: str | None = None,
    conversation_history: list | None = None,
    customer_data: dict | None = None,
) -> str:

    conversation_history = conversation_history or []
    customer_data = customer_data or {}

    language = detect_language(
        customer_message
    )

    language_name = (
        "кыргызском языке"
        if language == "kyrgyz"
        else "русском языке"
    )

    if next_question:

        instruction = f"""
СИСТЕМА УЖЕ ОПРЕДЕЛИЛА СЛЕДУЮЩИЙ ВОПРОС:

{next_question}

Сформулируй этот вопрос естественно
на {language_name}.

ВАЖНО:
- Не отвечай на вопрос.
- Не добавляй никаких новых сведений.
- Не добавляй числа.
- Не добавляй цены.
- Не добавляй диапазоны.
- Не добавляй валюты.
- Не объясняй, зачем нужен ответ.
- Не меняй смысл вопроса.

Верни только один готовый вопрос.
"""

    else:

        instruction = f"""
Система сообщает, что обязательная информация получена.

Кратко поблагодари клиента на {language_name}.

Не добавляй никаких новых сведений.
Не обещай одобрение.
Не сообщай условия займа.
Верни только короткое сообщение.
"""

    history_text = ""

    for item in conversation_history:

        role = item.get("role", "")
        content = item.get("content", "")

        if not content:
            continue

        if role == "customer":
            history_text += f"Клиент: {content}\n"

        elif role == "assistant":
            history_text += f"Айлин: {content}\n"

    if not history_text:
        history_text = "История отсутствует."

    customer_data_text = ""

    for key, value in customer_data.items():

        if value is not None:
            customer_data_text += f"{key}: {value}\n"

    if not customer_data_text:
        customer_data_text = "Данные отсутствуют."

    prompt = f"""
{SYSTEM_PROMPT}

ЯЗЫК ОТВЕТА:
{language_name}

ИСТОРИЯ:
{history_text}

ДАННЫЕ КЛИЕНТА:
{customer_data_text}

ПОСЛЕДНЕЕ СООБЩЕНИЕ КЛИЕНТА:
{customer_message}

ИНСТРУКЦИЯ СИСТЕМЫ:
{instruction}

Верни только готовое сообщение Айлин.
"""

    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "stream": False,
        "options": {
            "temperature": 0,
        },
    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()

    except requests.RequestException as error:

        raise RuntimeError(
            f"Ollama connection error: {error}"
        ) from error

    try:

        answer = (
            data["message"]["content"]
            .strip()
        )

    except (
        KeyError,
        TypeError,
    ) as error:

        raise RuntimeError(
            f"Unexpected Ollama response: {data}"
        ) from error

    if not answer:

        raise RuntimeError(
            "Ollama returned an empty response."
        )

    return answer

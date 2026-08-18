# ============================================================
# QUESTIONS
# ============================================================

QUESTIONS_RU = {

    "car_model":
        "Подскажите, пожалуйста, модель автомобиля?",

    "car_year":
        "Какого года ваш автомобиль?",

    "car_value":
        "Какова примерная стоимость автомобиля?",

    "loan_amount":
        "Какую сумму займа вы хотите получить?",

    "loan_program":
        "Какую программу займа вы рассматриваете?",

    "vehicle_possession":
        "Подскажите, пожалуйста, Вас интересует займ без изъятия автомобиля или с размещением автомобиля на охраняемой стоянке?",

    "registration_region":
        "В каком регионе вы зарегистрированы?",

    "loan_term_months":
        "На какой срок вы хотите оформить займ?",
}


QUESTIONS_KY = {

    "car_model":
        "Унааңыздын моделин айтып бересизби?",

    "car_year":
        "Унааңыз кайсы жылы чыгарылган?",

    "car_value":
        "Унааңыздын болжолдуу баасы канча?",

    "loan_amount":
        "Канча сом өлчөмүндө насыя алууну каалайсыз?",

    "loan_program":
        "Кайсы насыя программасын карап жатасыз?",

    "vehicle_possession":
        "Унаа өзүңүздө калуучу насыяны каалайсызбы же унааны кайтаруу жайына жайгаштыруу менен насыя алууну каалайсызбы?",

    "registration_region":
        "Кайсы аймакта катталгансыз?",

    "loan_term_months":
        "Насыяны канча мөөнөткө алууну каалайсыз?",
}


# ============================================================
# LANGUAGE DETECTION
# ============================================================

def detect_language(text: str) -> str:
    """
    Detect Russian vs Kyrgyz using deterministic markers.

    Avoid single-letter markers because they can appear naturally
    inside Russian words.
    """

    if not text:
        return "russian"

    text_lower = text.lower()

    # Strong Kyrgyz words/phrases.
    kyrgyz_words = [
        "менин",
        "сенин",
        "биздин",
        "силердин",
        "унаа",
        "унаам",
        "унаанын",
        "автоунаа",
        "жылкы",
        "жылы",
        "канча",
        "болжолдуу",
        "баасы",
        "насыя",
        "зайым",
        "катталган",
        "кайсы",
        "аймакта",
        "каалайсызбы",
        "алууну",
        "каалайм",
        "алгым",
    ]

    # Kyrgyz-specific letters are strong evidence.
    kyrgyz_letters = [
        "ө",
        "ү",
        "ң",
        "ғ",
        "қ",
        "һ",
    ]

    for letter in kyrgyz_letters:
        if letter in text_lower:
            return "kyrgyz"

    # Check words rather than arbitrary substrings.
    import re

    words = set(
        re.findall(
            r"[а-яёңөүғқһ]+",
            text_lower,
        )
    )

    for word in kyrgyz_words:
        if word in words:
            return "kyrgyz"

    return "russian"


# ============================================================
# QUESTION GENERATOR
# ============================================================

def generate_question(
    field: str,
    language: str = "russian",
) -> str | None:
    """
    Return a deterministic question in the customer's language.
    """

    if language == "kyrgyz":
        return QUESTIONS_KY.get(field)

    return QUESTIONS_RU.get(field)


# ============================================================
# REQUIRED FIELDS
# ============================================================

REQUIRED_FIELDS = [

    "car_model",

    "car_year",

    "car_value",

    "loan_amount",

    "loan_program",

    "vehicle_possession",

    "registration_region",

    "loan_term_months",
]


# ============================================================
# NEXT QUESTION
# ============================================================

def generate_next_question(
    customer,
    language: str = "russian",
):
    """
    Return the question for the first missing required field.

    Return None when all required information is collected.
    """

    for field in REQUIRED_FIELDS:

        value = getattr(
            customer,
            field,
            None,
        )

        if value is None:

            return generate_question(
                field,
                language,
            )

    return None

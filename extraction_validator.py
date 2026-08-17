import re
from typing import Optional


RUSSIAN_NUMBER_WORDS = {
    "ноль": 0,
    "один": 1,
    "одна": 1,
    "одно": 1,
    "два": 2,
    "две": 2,
    "три": 3,
    "четыре": 4,
    "пять": 5,
    "шесть": 6,
    "семь": 7,
    "восемь": 8,
    "девять": 9,
    "десять": 10,
    "одиннадцать": 11,
    "двенадцать": 12,
}


def extract_loan_term_months(text: str) -> Optional[int]:
    """
    Extract loan duration in months from Russian customer messages.

    Examples:
        "на один месяц" -> 1
        "на 1 месяц" -> 1
        "на месяц" -> 1
        "на два месяца" -> 2
        "на 6 месяцев" -> 6
        "на 12 месяцев" -> 12
    """

    if not text:
        return None

    text_lower = text.lower().replace("ё", "е")

    # ---------------------------------------------------------
    # 1. Numeric forms:
    #    на 1 месяц
    #    на 2 месяца
    #    на 12 месяцев
    # ---------------------------------------------------------
    numeric_pattern = re.compile(
        r"\bна\s+(\d{1,2})\s+"
        r"(?:месяц|месяца|месяцев)\b",
        re.IGNORECASE,
    )

    match = numeric_pattern.search(text_lower)

    if match:
        months = int(match.group(1))

        if 1 <= months <= 60:
            return months

    # ---------------------------------------------------------
    # 2. Word forms:
    #    на один месяц
    #    на два месяца
    #    на три месяца
    # ---------------------------------------------------------
    word_pattern = re.compile(
        r"\bна\s+("
        + "|".join(RUSSIAN_NUMBER_WORDS.keys())
        + r")\s+"
        r"(?:месяц|месяца|месяцев)\b",
        re.IGNORECASE,
    )

    match = word_pattern.search(text_lower)

    if match:
        word = match.group(1).lower()
        return RUSSIAN_NUMBER_WORDS[word]

    # ---------------------------------------------------------
    # 3. Short natural form:
    #    на месяц
    # ---------------------------------------------------------
    if re.search(
        r"\bна\s+месяц\b",
        text_lower,
        re.IGNORECASE,
    ):
        return 1

    # ---------------------------------------------------------
    # 4. Alternative phrasing:
    #    срок один месяц
    #    срок: 1 месяц
    #    срок займа один месяц
    # ---------------------------------------------------------
    alternative_numeric = re.search(
        r"\b(?:срок|срок займа|срок кредита)"
        r"\s*:?\s*(\d{1,2})\s+"
        r"(?:месяц|месяца|месяцев)\b",
        text_lower,
        re.IGNORECASE,
    )

    if alternative_numeric:
        months = int(alternative_numeric.group(1))

        if 1 <= months <= 60:
            return months

    alternative_word = re.search(
        r"\b(?:срок|срок займа|срок кредита)"
        r"\s*:?\s*("
        + "|".join(RUSSIAN_NUMBER_WORDS.keys())
        + r")\s+"
        r"(?:месяц|месяца|месяцев)\b",
        text_lower,
        re.IGNORECASE,
    )

    if alternative_word:
        return RUSSIAN_NUMBER_WORDS[
            alternative_word.group(1).lower()
        ]

    return None
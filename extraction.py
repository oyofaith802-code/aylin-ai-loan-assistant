from __future__ import annotations

import re
from typing import Any, Dict, Optional


# ============================================================
# FIELDS
# ============================================================

FIELDS = [
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
# TEXT CLEANING
# ============================================================

def _clean_text(text: str) -> str:
    if not text:
        return ""

    text = str(text)

    # Normalize special spaces
    text = text.replace("\xa0", " ")
    text = text.replace("\u202f", " ")

    # Normalize dash characters
    text = text.replace("–", "-")
    text = text.replace("—", "-")

    # Collapse whitespace
    text = re.sub(r"[ \t\r\n]+", " ", text)

    return text.strip()


# ============================================================
# NUMBER NORMALIZATION
# ============================================================

def _normalize_number(value: Any) -> Optional[float]:
    if value is None:
        return None

    if isinstance(value, (int, float)):
        try:
            number = float(value)

            if number != number:
                return None

            return number

        except (TypeError, ValueError):
            return None

    value = str(value).strip().lower()

    if not value:
        return None

    value = value.replace("\xa0", " ")
    value = value.replace("\u202f", " ")

    # --------------------------------------------------------
    # MILLIONS
    # --------------------------------------------------------

    million_match = re.search(
        r"(\d+(?:[.,]\d+)?)\s*"
        r"(?:млн|миллион|миллиона|миллионов|"
        r"million|millions)\b",
        value,
        flags=re.IGNORECASE,
    )

    if million_match:
        raw = million_match.group(1)

        try:
            number = float(raw.replace(",", "."))
            return number * 1_000_000
        except ValueError:
            return None

    # --------------------------------------------------------
    # THOUSANDS
    # --------------------------------------------------------

    # 400,000
    if re.fullmatch(
        r"\d{1,3}(?:,\d{3})+",
        value,
    ):
        try:
            return float(value.replace(",", ""))
        except ValueError:
            return None

    # 400.000
    if re.fullmatch(
        r"\d{1,3}(?:\.\d{3})+",
        value,
    ):
        try:
            return float(value.replace(".", ""))
        except ValueError:
            return None

    # 400 000
    if re.fullmatch(
        r"\d{1,3}(?:\s\d{3})+",
        value,
    ):
        try:
            return float(value.replace(" ", ""))
        except ValueError:
            return None

    # --------------------------------------------------------
    # NORMAL NUMBER / DECIMAL
    # --------------------------------------------------------

    normalized = value.replace(" ", "")

    # Decimal comma
    normalized = normalized.replace(",", ".")

    try:
        return float(normalized)
    except ValueError:
        return None


# ============================================================
# NATURAL RUSSIAN MONEY EXTRACTION
# ============================================================

def _extract_natural_money(text: str) -> Optional[float]:
    """
    Handles natural Russian money expressions such as:

        миллион двести
        миллион двести тысяч
        тысяч 500
        тысячи 500
        500 тысяч
    """

    text = _clean_text(text).lower()

    # --------------------------------------------------------
    # "миллион двести" -> 1,200,000
    # --------------------------------------------------------

    match = re.search(
        r"\bмиллион(?:а|ов)?\s+"
        r"(сто|двести|триста|четыреста|пятьсот|"
        r"шестьсот|семьсот|восемьсот|девятьсот)"
        r"(?:\s+(тысяч|тысяча|тысячи))?\b",
        text,
        flags=re.IGNORECASE,
    )

    if match:
        hundreds = {
            "сто": 100,
            "двести": 200,
            "триста": 300,
            "четыреста": 400,
            "пятьсот": 500,
            "шестьсот": 600,
            "семьсот": 700,
            "восемьсот": 800,
            "девятьсот": 900,
        }

        return 1_000_000 + hundreds[match.group(1).lower()] * 1_000

    # --------------------------------------------------------
    # "тысяч 500" / "тысячи 500" -> 500,000
    # --------------------------------------------------------

    match = re.search(
        r"\b(?:тысяч|тысяча|тысячи)\s+"
        r"(\d+(?:[.,]\d+)?)\b",
        text,
        flags=re.IGNORECASE,
    )

    if match:
        try:
            return float(match.group(1).replace(",", ".")) * 1_000
        except ValueError:
            pass

    return None


# ============================================================
# MONEY PATTERN
# ============================================================

_MONEY_NUMBER = r"\d[\d\s,.]*"

_MONEY_PATTERN = (
    r"("
    + _MONEY_NUMBER
    + r")"
    r"\s*"
    r"(?:сом|сомов|сомах|сома)"
    r"\b"
)


# ============================================================
# MONEY EXTRACTION HELPER
# ============================================================

def _extract_first_money(
    text: str,
    pattern: str,
) -> Optional[float]:

    match = re.search(
        pattern,
        text,
        flags=re.IGNORECASE,
    )

    if not match:
        return None

    raw = match.group(1)

    return _normalize_number(raw)


# ============================================================
# LOAN AMOUNT
# ============================================================

def _extract_loan_amount(
    text: str,
) -> Optional[float]:

    text = _clean_text(text)

    # If the message clearly describes the vehicle's price/value,
    # do not interpret that amount as the requested loan amount.
    if re.search(
        r"машин|автомобил|стоит|цена|стоимость|по деньгам",
        text,
        flags=re.IGNORECASE,
    ) and not re.search(
        r"получить|хочу|хотим|нужно|нужен|займ|сумма",
        text,
        flags=re.IGNORECASE,
    ):
        return None

    natural_money = _extract_natural_money(text)

    if natural_money is not None and natural_money > 0:
        # Only use the natural form here when the message clearly
        # expresses a requested loan amount.
        if re.search(
            r"получить|хочу|хотим|нужно|нужен|получить",
            text,
            flags=re.IGNORECASE,
        ):
            return natural_money

    # --------------------------------------------------------
    # STRONG LOAN REQUEST PATTERNS
    #
    # These should be checked BEFORE generic money patterns.
    # --------------------------------------------------------

    strong_patterns = [

        # Мы хотели бы получить под него 400 000 сом
        r"(?:мы\s+)?хотели\s+бы\s+получить"
        r"(?:\s+под\s+него|\s+под\s+автомобиль)?"
        r"\D{0,80}"
        + _MONEY_PATTERN,

        # Мы хотим получить 400 000 сом
        r"(?:мы\s+)?хотим\s+получить"
        r"\D{0,80}"
        + _MONEY_PATTERN,

        # Я хочу получить 400 000 сом
        r"(?:я\s+)?хочу\s+получить"
        r"\D{0,80}"
        + _MONEY_PATTERN,

        # Нам нужно 400 000 сом
        r"(?:нам\s+)?нужно"
        r"\D{0,60}"
        + _MONEY_PATTERN,

        # Нам нужен займ 400 000 сом
        r"(?:нам\s+)?нужен"
        r"\D{0,60}"
        + _MONEY_PATTERN,

        # Получить 400 000 сом
        r"получить"
        r"\D{0,80}"
        + _MONEY_PATTERN,

        # Выдать нам 400 000 сом
        r"выдать"
        r"\D{0,80}"
        + _MONEY_PATTERN,

        # Запрашиваем 400 000 сом
        r"запрашиваем"
        r"\D{0,80}"
        + _MONEY_PATTERN,

        # Запрошенная сумма 400 000 сом
        r"запрошенн(?:ая|ую|ой)?\s+сумма"
        r"\D{0,50}"
        + _MONEY_PATTERN,

        # Хочу 400 000 сом
        r"(?:я\s+)?хочу"
        r"\D{0,60}"
        + _MONEY_PATTERN,

        # Хотим 400 000 сом
        r"(?:мы\s+)?хотим"
        r"\D{0,60}"
        + _MONEY_PATTERN,
    ]

    for pattern in strong_patterns:

        value = _extract_first_money(
            text,
            pattern,
        )

        if value is not None and value > 0:
            return value

    # --------------------------------------------------------
    # THOUSANDS / MILLIONS
    #
    # Examples:
    #   20 тыс
    #   20 тыс долларов
    #   20 тысяч долларов
    #   20к долларов
    #   500 тыс сом
    #   1.5 млн сом
    #   1,5 млн долларов
    # --------------------------------------------------------

    scaled_money_patterns = [

        # 1.5 млн
        r"\b(\d+(?:[.,]\d+)?)\s*"
        r"(?:млн\.?|миллион(?:а|ов)?)"
        r"(?:\s+(?:сом|сома|сомов|"
        r"доллар|доллара|долларов|usd|"
        r"евро|тенге))?\b",

        # 500 тыс / 500 тысяч / 500к / 500 миң
        r"\b(\d+(?:[.,]\d+)?)\s*"
        r"(?:тыс\.?|тысяч|тысяча|тысячи|к|миң)"
        r"(?:\s+(?:сом|сома|сомов|"
        r"доллар|доллара|долларов|usd|"
        r"евро|тенге))?\b",
    ]

    for pattern in scaled_money_patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if not match:
            continue

        number = match.group(1)

        try:
            base = float(
                number.replace(",", ".")
            )

        except (TypeError, ValueError):
            continue

        multiplier = 1_000_000 if re.search(
            r"(млн|миллион)",
            match.group(0),
            flags=re.IGNORECASE,
        ) else 1_000

        value = base * multiplier

        if value > 0:
            return value

    # --------------------------------------------------------
    # LABELED LOAN AMOUNT PATTERNS
    # --------------------------------------------------------

    labeled_patterns = [

        # Сумма: 400 000 сом
        r"(?:сумма|сумму)"
        r"\D{0,50}"
        + _MONEY_PATTERN,

        # Займ: 400 000 сом
        r"(?:займ|займа)"
        r"\D{0,50}"
        + _MONEY_PATTERN,

        # Получение: 400 000 сом
        r"получени[ея]"
        r"\D{0,60}"
        + _MONEY_PATTERN,

        # Размер займа: 400 000 сом
        r"размер\s+(?:займа|кредита)"
        r"\D{0,50}"
        + _MONEY_PATTERN,

        # Сумма займа: 400 000 сом
        r"сумма\s+(?:займа|кредита)"
        r"\D{0,50}"
        + _MONEY_PATTERN,
    ]

    for pattern in labeled_patterns:

        value = _extract_first_money(
            text,
            pattern,
        )

        if value is not None and value > 0:
            return value

    # ========================================================
    # SAFER FALLBACK
    # ========================================================
    #
    # IMPORTANT:
    #
    # Do NOT automatically interpret a car price as a loan.
    #
    # Example:
    #
    # "Примерная стоимость автомобиля 1 500 000 сом."
    #
    # Result:
    #
    # car_value   = 1 500 000
    # loan_amount = None
    #
    # ========================================================

    car_value_context = re.compile(
        r"(?:"
        r"стоимость"
        r"|цена"
        r"|рыночная\s+стоимость"
        r"|примерная\s+стоимость"
        r"|автомобиль\s+стоит"
        r"|машина\s+стоит"
        r"|автомобиль\s+оценивается"
        r"|машина\s+оценивается"
        r")",
        flags=re.IGNORECASE,
    )

    if car_value_context.search(text):
        return None

    # --------------------------------------------------------
    # Standalone money fallback
    #
    # Examples:
    #
    # 400 000 сом
    # 400000 сом
    # 400,000 сом
    #
    # This is only used when the text does NOT look like
    # a vehicle-price statement.
    # --------------------------------------------------------

    matches = re.finditer(
        _MONEY_PATTERN,
        text,
        flags=re.IGNORECASE,
    )

    for match in matches:

        value = _normalize_number(
            match.group(1)
        )

        if value is not None and value > 0:
            return value

    return None


# ============================================================
# LOAN TERM
# ============================================================

def _extract_loan_term(
    text: str,
) -> Optional[int]:

    text = _clean_text(text)

    # --------------------------------------------------------
    # RUSSIAN NUMERIC MONTHS
    # --------------------------------------------------------

    patterns = [
        r"\bна\s+(\d+)\s+(?:месяц|месяца|месяцев)\b",
        r"\b(\d+)\s+(?:месяц|месяца|месяцев)\b",
        r"\bсрок(?:а)?\s*[:\-]?\s*(\d+)\s+(?:месяц|месяца|месяцев)\b",
        r"\bсрок\s*[:\-]?\s*(\d+)\b",
    ]

    # --------------------------------------------------------
    # RUSSIAN NATURAL YEAR EXPRESSIONS
    # --------------------------------------------------------
    #
    # Examples:
    #   на год
    #   год
    #   на один год
    #   один год
    #
    # A loan term expressed as one year = 12 months.
    # --------------------------------------------------------

    if re.search(
        r"\bна\s+(?:один\s+)?год\b",
        text,
        flags=re.IGNORECASE,
    ):
        return 12

    if re.search(
        r"\b(?:один\s+)?год\b",
        text,
        flags=re.IGNORECASE,
    ):
        return 12

    if re.search(
        r"\bна\s+месяц\b",
        text,
        flags=re.IGNORECASE,
    ):
        return 1

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if not match:
            continue

        try:
            months = int(match.group(1))

            if 1 <= months <= 120:
                return months

        except (ValueError, TypeError):
            pass

    # --------------------------------------------------------
    # KYRGYZ YEARS
    #
    # Examples:
    #   2 жылга алсам деп ойлоп жатам -> 24
    #   3 жылга алгым келет -> 36
    #   2 жылга -> 24
    # --------------------------------------------------------

    kyrgyz_year_match = re.search(
        r"\b(\d+)\s*(?:жыл|жылга)\b",
        text,
        flags=re.IGNORECASE,
    )

    if kyrgyz_year_match:

        try:
            years = int(kyrgyz_year_match.group(1))
            months = years * 12

            if 1 <= months <= 120:
                return months

        except (ValueError, TypeError):
            pass

    # --------------------------------------------------------
    # KYRGYZ MONTHS
    #
    # Examples:
    #   24 айга алгым келет -> 24
    #   12 айга -> 12
    # --------------------------------------------------------

    kyrgyz_month_match = re.search(
        r"\b(\d+)\s*(?:ай|айга)\b",
        text,
        flags=re.IGNORECASE,
    )

    if kyrgyz_month_match:

        try:
            months = int(kyrgyz_month_match.group(1))

            if 1 <= months <= 120:
                return months

        except (ValueError, TypeError):
            pass

    # --------------------------------------------------------
    # WORD NUMBERS
    # --------------------------------------------------------

    word_numbers = {
        "один": 1,
        "два": 2,
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
        "тринадцать": 13,
        "четырнадцать": 14,
        "пятнадцать": 15,
        "шестнадцать": 16,
        "семнадцать": 17,
        "восемнадцать": 18,
        "девятнадцать": 19,
        "двадцать": 20,
        "тридцать": 30,
        "сорок": 40,
        "пятьдесят": 50,
        "шестьдесят": 60,
        "семьдесят": 70,
        "восемьдесят": 80,
        "девяносто": 90,
        "сто": 100,
    }

    for word, number in word_numbers.items():

        pattern = (
            rf"\b(?:на\s+)?{word}\s+"
            r"(?:месяц|месяца|месяцев)\b"
        )

        if re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        ):
            return number

    return None


# ============================================================
# CAR YEAR
# ============================================================

def _extract_car_year(
    text: str,
) -> Optional[int]:

    text = _clean_text(text)

    # --------------------------------------------------------
    # FULL YEARS
    #
    # Examples:
    #   2021
    #   2021 года
    #   2021 год
    #   2021 г.
    #   2021-жылкы
    # --------------------------------------------------------

    full_year_pattern = (
        r"\b"
        r"(19\d{2}|20\d{2})"
        r"\s*"
        r"(?:года|год|г\.|жылкы|жыл)?"
        r"\b"
    )

    for match in re.finditer(
        full_year_pattern,
        text,
        flags=re.IGNORECASE,
    ):

        year = int(match.group(1))

        if 1980 <= year <= 2035:
            return year

    # --------------------------------------------------------
    # CONVERSATIONAL TWO-DIGIT YEARS
    #
    # Examples:
    #   21 года
    #   21-го года
    #   21-й год
    #   21 г.
    #   21-жылкы
    # --------------------------------------------------------

    short_year_pattern = (
        r"\b"
        r"(\d{2})"
        r"(?:-?го|-?й)?"
        r"\s*"
        r"(?:года|год|г\.|-?жылкы|-?жыл)"
        r"(?=\s|$|[.!?,])"
    )

    for match in re.finditer(
        short_year_pattern,
        text,
        flags=re.IGNORECASE,
    ):

        short_year = int(match.group(1))

        if 0 <= short_year <= 35:
            return 2000 + short_year

    return None


# ============================================================
# CAR VALUE
# ============================================================

def _extract_car_value(
    text: str,
) -> Optional[float]:

    text = _clean_text(text)

    # Natural expressions such as:
    # "машина где-то миллион двести стоит"
    natural_money = _extract_natural_money(text)

    if natural_money is not None and natural_money > 0:
        if re.search(
            r"машин|автомобил|стоит|цена|стоимость|по деньгам",
            text,
            flags=re.IGNORECASE,
        ):
            return natural_money

    # Explicit scaled car value:
    # "Машина стоит 1.5 млн сом" -> 1500000
    car_scaled_match = re.search(
        r"\b(\d+(?:[.,]\d+)?)\s*"
        r"(?:млн\.?|миллион(?:а|ов)?)"
        r"(?:\s+(?:сом|сома|сомов))?\b",
        text,
        flags=re.IGNORECASE,
    )

    if car_scaled_match and re.search(
        r"машин|автомобил|стоит|цена|стоимость|по деньгам",
        text,
        flags=re.IGNORECASE,
    ):
        return float(
            car_scaled_match.group(1).replace(",", ".")
        ) * 1_000_000

    patterns = [

        # ----------------------------------------------------
        # FOREIGN CURRENCY / NATURAL CUSTOMER ANSWERS
        # ----------------------------------------------------
        # 20 тыс долларов
        # 20 тысяч долларов
        # 20 тыс. долларов
        r"(\\d+(?:[.,]\\d+)?)"
        r"\\s*(?:тысяч|тыс\\.?)"
        r"\\s*(?:доллар(?:ов|а)?|usd|\\$)\\b",

        # 20 000 долларов
        # 20000 долларов
        r"("
        + _MONEY_NUMBER
        + r")"
        r"\\s*(?:доллар(?:ов|а)?|usd)\\b",

        # 20 тыс сом
        # 20 тысяч сом
        r"(\\d+(?:[.,]\\d+)?)"
        r"\\s*(?:тысяч|тыс\\.?)"
        r"\\s*сом\\b",

        # 1.5 млн долларов / 1.5 миллиона долларов
        r"(\\d+(?:[.,]\\d+)?)"
        r"\\s*(?:млн|миллион(?:а|ов)?)"
        r"\\s*(?:доллар(?:ов|а)?|usd|\\$)\\b",

        # ----------------------------------------------------
        # EXISTING SOM PATTERNS
        # ----------------------------------------------------

        # Примерная стоимость автомобиля 1 500 000 сом
        r"(?:примерная\s+)?"
        r"(?:стоимость|цена)"
        r"(?:\s+автомобиля)?"
        r"(?:\s+составляет|\s+около|\s*[:\-]?)"
        r"\s*"
        r"("
        + _MONEY_NUMBER
        + r")"
        r"\s*сом\b",

        # Рыночная стоимость 1 500 000 сом
        r"(?:рыночная\s+)?стоимость"
        r"\D{0,60}"
        r"("
        + _MONEY_NUMBER
        + r")"
        r"\s*сом\b",

        # Цена автомобиля: 1 500 000 сом
        r"цена"
        r"\D{0,60}"
        r"("
        + _MONEY_NUMBER
        + r")"
        r"\s*сом\b",

        # Автомобиль стоит 1 500 000 сом
        r"(?:автомобиль|машина)"
        r"\s+(?:стоит|оценивается)"
        r"\D{0,30}"
        r"("
        + _MONEY_NUMBER
        + r")"
        r"\s*сом\b",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if not match:
            continue

        value = _normalize_number(
            match.group(1)
        )

        if value is not None and value > 0:
            return value

    return None


# ============================================================
# CAR MODEL
# ============================================================

_BAD_MODEL_VALUES = {

    "возможно",
    "возможно ли",
    "да",
    "нет",
    "новый",
    "новая",
    "новое",
    "современный",
    "современная",
    "современное",
    "автомобиль",
    "машина",
    "это возможно",
    "автомобиля",
    "машины",
    "хороший",
    "хорошая",
}


def _is_valid_car_model(
    model: Any,
) -> bool:

    if model is None:
        return False

    if not isinstance(model, str):
        return False

    model = _clean_text(model)

    if not model:
        return False

    lower = model.lower().strip()

    # --------------------------------------------------------
    # NEVER ACCEPT VEHICLE-POSSESSION PHRASES AS CAR MODELS
    # --------------------------------------------------------

    invalid_possession_phrases = {
        "без передачи автомобиля",
        "без передачи машины",
        "без передачи авто",
        "без изъятия автомобиля",
        "без изъятия машины",
        "без изъятия авто",
        "без изъятия транспортного средства",
        "без изъятия",
        "без передачи",
    }

    if lower in invalid_possession_phrases:
        return False

    if lower.startswith("без передачи "):
        return False

    if lower.startswith("без изъятия "):
        return False

    # --------------------------------------------------------
    # NEVER ACCEPT GENERIC / NON-MODEL VALUES
    # --------------------------------------------------------

    invalid_values = {
        "бишкек",
        "ош",
        "чуй",
        "чуйская область",
        "ошская область",
        "иссык-куль",
        "иссык куль",
        "иссык-кульская область",
        "нарын",
        "нарынская область",
        "талас",
        "таласская область",
        "джалал-абад",
        "джалал абад",
        "джалал-абадская область",
        "баткен",
        "баткенская область",
        "возможно",
        "можно",
        "хотим",
        "хотели",
        "хочу",
        "нужно",
        "нужен",
        "нужна",
        "нужны",
        "получить",
        "получим",
        "автомобиль",
        "машина",
        "машину",
        "машины",
        "машиной",
        "новая",
        "новый",
        "новое",
        "новые",
        "современная",
        "современный",
        "современное",
        "современные",
        "вот",
        "это",
        "там",
        "здесь",
        "да",
        "нет",
        "нормально",
        "хорошо",

        # Location / registration words.
        "бишкек",
        "ош",
        "нарын",
        "талас",
        "баткен",
        "чуй",
        "иссык-куль",
        "джалал-абад",
    }

    if lower in invalid_values:
        return False

    # --------------------------------------------------------
    # MONEY / CURRENCY MUST NEVER BE A CAR MODEL
    # --------------------------------------------------------

    money_words = (
        "сом",
        "сома",
        "сомов",
        "тыс",
        "тысяч",
        "тысяча",
        "тысячи",
        "млн",
        "миллион",
        "миллиона",
        "миллионов",
        "доллар",
        "доллара",
        "долларов",
        "usd",
        "евро",
        "рубль",
        "рубля",
        "рублей",
        "тенге",
        "€",
        "$",
        "₽",
    )

    if any(
        re.search(
            rf"\b{re.escape(word)}\b",
            lower,
            flags=re.IGNORECASE,
        )
        for word in money_words
        if word.isalnum()
    ):
        return False

    # Currency symbols.
    if any(symbol in model for symbol in ("$", "€", "₽")):
        return False

    # --------------------------------------------------------
    # PURE / MONEY-LIKE NUMERIC VALUES
    # --------------------------------------------------------

    if re.fullmatch(
        r"\d+(?:[\s,.]\d+)*",
        lower,
    ):
        return False

    if re.fullmatch(
        r"\d+(?:[.,]\d+)?\s*(?:к|k)",
        lower,
        flags=re.IGNORECASE,
    ):
        return False

    # --------------------------------------------------------
    # REGIONS / CITIES ARE NOT CAR MODELS
    # --------------------------------------------------------

    invalid_regions = {
        "бишкек",
        "ош",
        "чуй",
        "чуйская область",
        "ошская область",
        "иссык-куль",
        "иссык куль",
        "иссык-кульская область",
        "нарын",
        "нарынская область",
        "талас",
        "таласская область",
        "джалал-абад",
        "джалал абад",
        "джалал-абадская область",
        "баткен",
        "баткенская область",
    }

    if lower in invalid_regions:
        return False

    # --------------------------------------------------------
    # GENERIC CONVERSATIONAL PREFIXES
    # --------------------------------------------------------

    invalid_starts = (
        "город:",
        "город ",
        "регион:",
        "регион ",
        "область:",
        "область ",
        "регистрация:",
        "регистрация ",
        "возможно ",
        "можно ",
        "хотим ",
        "хотели ",
        "хочу ",
        "нужно ",
        "нужен ",
        "нужна ",
        "нужны ",
        "получ",
        "нам нужно ",
        "мы хотим ",
        "мы хотели ",
        "я хочу ",
        "у нас нужно ",

        # Registration/location sentences are NOT car models.
        "я зарегистрирован ",
        "я зарегистрирована ",
        "зарегистрирован ",
        "зарегистрирована ",
        "я прописан ",
        "я прописана ",
        "прописан ",
        "прописана ",
        "регистрация ",
        "регион ",
        "город ",
        "область ",
    )

    if lower.startswith(invalid_starts):
        return False

    # --------------------------------------------------------
    # SENTENCE-LIKE VALUES
    # --------------------------------------------------------

    if len(model) > 60:
        return False

    if re.search(
        r"\b(?:сом|сома|сомов|"
        r"тыс|тысяч|тысяча|тысячи|"
        r"млн|миллион|миллиона|миллионов|"
        r"доллар|доллара|долларов|usd|"
        r"месяц|месяца|месяцев|"
        r"получить|получим|нужно|нужен|нужна|нужны|"
        r"хотим|хотели|хочу|займ|залог|стоимость|"
        r"цена|автомобиль|машина|машину|машины|"
        r"примерная|примерно|регион|регистрация|"
        r"город|область|документы|"
        r"подписываем|собственники)\b",
        lower,
        flags=re.IGNORECASE,
    ):
        return False

    # --------------------------------------------------------
    # TOO MANY WORDS = PROBABLY A SENTENCE
    # --------------------------------------------------------

    words = re.findall(
        r"[A-Za-zА-Яа-яЁё0-9]+",
        model,
    )

    if len(words) > 5:
        return False

    # --------------------------------------------------------
    # MUST CONTAIN ALPHANUMERIC CONTENT
    # --------------------------------------------------------

    if not re.search(
        r"[A-Za-zА-Яа-яЁё0-9]",
        model,
    ):
        return False

    return True


def _extract_car_model(
    text: str,
) -> Optional[str]:

    text = _clean_text(text)

    # --------------------------------------------------------
    # REMOVE GREETING PREFIXES BEFORE ANY MODEL EXTRACTION
    #
    # Greetings must never become part of car_model.
    #
    # Examples:
    #   "Здравствуйте"
    #       -> None
    #
    #   "Здравствуйте Toyota Camry 2021 года"
    #       -> "Toyota Camry 2021 года"
    #
    #   "Салам Toyota Camry 2021 года"
    #       -> "Toyota Camry 2021 года"
    # --------------------------------------------------------

    greeting_prefixes = [
        "здравствуйте",
        "здравствуй",
        "добрый день",
        "доброе утро",
        "добрый вечер",
        "привет",
        "салам",
        "саламатсызбы",
    ]

    lower_text = text.lower().strip()

    # Message is only a greeting.
    if lower_text in greeting_prefixes:
        return None

    # Remove greeting followed by whitespace or punctuation.
    for greeting in greeting_prefixes:

        pattern = (
            rf"^{re.escape(greeting)}"
            rf"(?:\s+|[,!?.:]+\s*)"
        )

        cleaned = re.sub(
            pattern,
            "",
            text,
            count=1,
            flags=re.IGNORECASE,
        ).strip()

        if cleaned != text.strip():
            text = cleaned
            break

    if not text:
        return None

    patterns = [

        # "Это BYD Song Plus"
        r"\bэто\s+"
        r"([A-Za-zА-Яа-яЁё0-9]"
        r"[A-Za-zА-Яа-яЁё0-9 .\-]{1,50}?)"
        r"(?=\s*(?:[.!?,]|$))",

        # "Модель: BYD Song Plus"
        r"(?:модель)"
        r"\s*[:\-]?\s*"
        r"([A-Za-zА-Яа-яЁё0-9]"
        r"[A-Za-zА-Яа-яЁё0-9 .\-]{1,50}?)"
        r"(?=\s*(?:[.!?,]|$))",

        # "Автомобиль: BYD Song Plus"
        r"(?:автомобиль|машина)"
        r"\s*[:\-]\s*"
        r"([A-Za-zА-Яа-яЁё0-9]"
        r"[A-Za-zА-Яа-яЁё0-9 .\-]{1,50}?)"
        r"(?=\s*(?:[.!?,]|$))",

        # "У меня BYD Song Plus"
        r"(?:у\s+меня|у\s+нас)"
        r"\s+"
        r"([A-Za-zА-Яа-яЁё0-9]"
        r"[A-Za-zА-Яа-яЁё0-9 .\-]{1,50}?)"
        r"(?=\s*(?:[.!?,]|$))",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if not match:
            continue

        model = _clean_text(match.group(1))

        # Remove year and its Russian/Kyrgyz suffix.
        model = re.sub(
            r"\s*(?:19\d{2}|20\d{2})"
            r"\s*[-–—]?\s*"
            r"(?:года|год|г\.?|жылкы|жыл)?"
            r"\s*$",
            "",
            model,
            flags=re.IGNORECASE,
        ).strip()

        # Remove leftover suffixes.
        model = re.sub(
            r"\s*[-–—]?\s*(?:жылкы|жыл|года|год|г\.?)\s*$",
            "",
            model,
            flags=re.IGNORECASE,
        ).strip()

        # Remove conversational two-digit year.
        #
        # Examples:
        #   Камри 21 года
        #   Камри 21-го года
        #   Камри 21-й год
        #   Камри 21 г.
        #
        model = re.sub(
            r"\s+\d{2}"
            r"(?:-?го|-?й)?"
            r"\s*"
            r"(?:года|год|г\.|жылкы|жыл)"
            r"\s*$",
            "",
            model,
            flags=re.IGNORECASE,
        ).strip()

        # Remove a short year left without its suffix.
        # This can happen when punctuation separates the
        # model and year.
        model = re.sub(
            r"\s+\d{2}(?:-?го|-?й)?\s*$",
            "",
            model,
            flags=re.IGNORECASE,
        ).strip()


        # Remove punctuation accidentally left before suffix.
        model = re.sub(
            r"\s*[-–—]\s*$",
            "",
            model,
        ).strip()

        # Remove trailing punctuation.
        model = re.sub(
            r"[.!?,:;]+$",
            "",
            model,
        ).strip()

        if _is_valid_car_model(model):
            return model

    # --------------------------------------------------------
    # REGISTRATION LOCATION MUST NEVER BE A CAR MODEL
    #
    # Customers often answer the registration question briefly:
    #   "Бишкек"
    #   "в Бишкеке"
    #   "Бостери"
    #   "в Бостери"
    #
    # Registration extraction already handles these values.
    # Therefore, stop car_model extraction from claiming them.
    # --------------------------------------------------------

    normalized_location = text.lower().strip(" .,!?;:")
    normalized_location = re.sub(
        r"^(?:в|на)\\s+",
        "",
        normalized_location,
        flags=re.IGNORECASE,
    ).strip()

    known_registration_locations = {
        "бишкек",
        "бишкеке",
        "бишкекте",
        "ош",
        "оше",
        "ошто",
        "чуй",
        "чуйда",
        "иссык-куль",
        "иссык куль",
        "иссык-куле",
        "нарын",
        "нарына",
        "нарында",
        "талас",
        "таласта",
        "джалал-абад",
        "джалал абад",
        "баткен",
        "баткенде",
        "бостери",
        "бостер",
        "бостериде",
    }

    if normalized_location in known_registration_locations:
        return None

    # --------------------------------------------------------
    # BARE CUSTOMER ANSWER
    #
    # Examples:
    #   Камри 2022 года
    #   Toyota Camry 2021
    #   Camry
    #
    # Do not treat ordinary conversational answers as models.
    # --------------------------------------------------------

    conversational_car_model_exclusions = [

        # Loan program names are NEVER car models.
        "автозалог",
        "автозайм",

        # Kyrgyz vehicle possession
        "машинаны өзүмдө калтыргым келет",
        "машинамды өзүмдө калтыргым келет",
        "унааны өзүмдө калтыргым келет",
        "унаамды өзүмдө калтыргым келет",
        "машина өзүмдө калсын",
        "машинам өзүмдө калсын",
        "унаа өзүмдө калсын",
        "унаам өзүмдө калсын",

        # Russian vehicle possession
        "машину хочу оставить у себя",
        "машина останется у меня",
        "автомобиль останется у меня",
        "хочу оставить машину у себя",
        "хочу оставить автомобиль у себя",

        # Kyrgyz registration
        "бишкекте катталгам",
        "ошто катталгам",
        "нарында катталгам",
        "таласта катталгам",
        "баткенде катталгам",
        "чуйда катталгам",

        # Russian registration
        "зарегистрирован в бишкеке",
        "зарегистрирована в бишкеке",
        "зарегистрирован в ош",
        "зарегистрирована в ош",
    ]

    # Kyrgyz registration phrases must never become car_model.
    conversational_car_model_exclusions.extend([

        "бишкекте катталганмын",
        "ошто катталганмын",
        "нарында катталганмын",
        "таласта катталганмын",
        "баткенде катталганмын",
        "чуйда катталганмын",

        "бишкекте катталгам",
        "ошто катталгам",
        "нарында катталгам",
        "таласта катталгам",
        "баткенде катталгам",
        "чуйда катталгам",

    ])

    lower_text = text.lower().strip()

    # --------------------------------------------------------
    # REGISTRATION DIRECT-ANSWER GUARD
    #
    # A customer may answer the registration question with only
    # a location, for example:
    #
    #   бостери
    #   в бостери
    #   бишкек
    #   в бишкеке
    #
    # These are registration answers, NOT car models.
    # --------------------------------------------------------

    registration_answer_patterns = [
        r"^в\\s+бостери$",
        r"^бостери$",
        r"^в\\s+бишкеке$",
        r"^бишкек$",
        r"^в\\s+ош(?:е)?$",
        r"^ош$",
        r"^в\\s+нарын(?:е)?$",
        r"^нарын$",
        r"^в\\s+талас(?:те)?$",
        r"^талас$",
        r"^в\\s+баткен(?:де)?$",
        r"^баткен$",
        r"^в\\s+чуй(?:да)?$",
        r"^чуй$",
    ]

    for pattern in registration_answer_patterns:
        if re.fullmatch(
            pattern,
            lower_text,
            flags=re.IGNORECASE,
        ):
            return None

    # --------------------------------------------------------
    # REMOVE GREETING PREFIXES
    #
    # Greetings are conversational text, not car models.
    #
    # Examples:
    #   "Здравствуйте"
    #       -> None
    #
    #   "Здравствуйте Toyota Camry 2021 года"
    #       -> "Toyota Camry 2021 года"
    #
    #   "Добрый день, Toyota Camry"
    #       -> "Toyota Camry"
    # --------------------------------------------------------

    greeting_prefixes = [
        "здравствуйте",
        "здравствуй",
        "добрый день",
        "доброе утро",
        "добрый вечер",
        "привет",
        "салам",
        "саламатсызбы",
    ]

    for greeting in greeting_prefixes:

        if lower_text == greeting:
            return None

        greeting_pattern = (
            rf"^{re.escape(greeting)}"
            rf"(?:\\s+|[,!?.:]\\s*)"
        )

        cleaned_text = re.sub(
            greeting_pattern,
            "",
            text,
            count=1,
            flags=re.IGNORECASE,
        ).strip()

        if cleaned_text != text.strip():

            text = cleaned_text
            lower_text = text.lower().strip()

            break

    # --------------------------------------------------------
    # ORDINARY CONVERSATIONAL SENTENCES MUST NEVER
    # BECOME CAR MODELS
    # --------------------------------------------------------

    conversational_sentence_patterns = [
        r"^я\\s+же\\s+написал$",
        r"^я\\s+же\\s+писал$",
        r"^я\\s+же\\s+сказал$",
        r"^я\\s+же\\s+говорил$",
        r"^я\\s+уже\\s+написал$",
        r"^я\\s+уже\\s+писал$",
        r"^я\\s+уже\\s+сказал$",
        r"^я\\s+уже\\s+говорил$",
        r"^мы\\s+же\\s+написали$",
        r"^мы\\s+уже\\s+написали$",
        r"^я\\s+не\\s+знаю$",
        r"^не\\s+знаю$",
        r"^не\\s+понял$",
        r"^не\\s+поняла$",
        r"^понятно$",
        r"^хорошо$",
        r"^ладно$",
        r"^ок$",
        r"^окей$",
        r"^да$",
        r"^нет$",
    ]

    for pattern in conversational_sentence_patterns:
        if re.fullmatch(
            pattern,
            lower_text,
            flags=re.IGNORECASE,
        ):
            return None

    # Common conversational phrases.
    conversational_phrases = {
        "я же написал",
        "я же писала",
        "я же написал вам",
        "я же писала вам",
        "я уже написал",
        "я уже написала",
        "я уже говорил",
        "я уже говорила",
        "я уже сказал",
        "я уже сказала",
        "я это уже написал",
        "я это уже сказала",
        "я это уже говорил",
        "я это уже говорила",
        "я вам уже написал",
        "я вам уже написала",
        "я вам уже говорил",
        "я вам уже говорила",
    }

    if lower_text in conversational_phrases:
        return None

    # --------------------------------------------------------
    # Additional Kyrgyz loan-term conversational answers.
    # These must never be interpreted as car models.
    loan_term_patterns = [
        r"\b\d+\s+жылга\b",
        r"\b\d+\s+жыл\b",
        r"\b\d+\s+айга\b",
        r"\b\d+\s+ай\b",
    ]

    for pattern in loan_term_patterns:

        if re.search(
            pattern,
            lower_text,
            flags=re.IGNORECASE,
        ):
            return None

    for phrase in conversational_car_model_exclusions:

        if phrase in lower_text:
            return None

    # Remove common greetings before checking the bare answer.
    #
    # Examples:
    #   "Здравствуйте Toyota Camry 2021 года"
    #       -> "Toyota Camry 2021 года"
    #
    #   "Здравствуйте"
    #       -> empty -> not a car model
    #
    # This prevents greetings from being stored as part of car_model.
    greeting_prefixes = [
        "здравствуйте",
        "здравствуй",
        "добрый день",
        "доброе утро",
        "добрый вечер",
        "привет",
        "салам",
        "саламатсызбы",
    ]

    bare = text.strip()

    for greeting in greeting_prefixes:

        pattern = (
            rf"^{re.escape(greeting)}"
            rf"(?:[,!?.:]|\\s)+"
        )

        cleaned = re.sub(
            pattern,
            "",
            bare,
            count=1,
            flags=re.IGNORECASE,
        )

        if cleaned != bare:
            bare = cleaned.strip()
            break

    # Remove full year + Russian/Kyrgyz year suffix.
    bare = re.sub(
        r"\b(?:19\d{2}|20\d{2})"
        r"\s*[-–—]?\s*"
        r"(?:года|год|г\.?|жылкы|жыл)?\b",
        "",
        bare,
        flags=re.IGNORECASE,
    )

    # Remove conversational two-digit vehicle years.
    #
    # Examples:
    #   Toyota Camry 21 года  -> Toyota Camry
    #   Камри 21-го года      -> Камри
    #   Камри 21-й год        -> Камри
    #   Камри 21 г.           -> Камри
    #   Toyota Camry 21-жылкы -> Toyota Camry
    #
    # The year extractor separately converts these to 2021.
    bare = re.sub(
        r"\b\d{2}"
        r"(?:-?го|-?й)?"
        r"\s*"
        r"(?:года|год|г\.|-?жылкы|-?жыл)"
        r"(?=\s|$|[.!?,])",
        "",
        bare,
        flags=re.IGNORECASE,
    )

    # Handle a remaining bare two-digit year at the end.
    bare = re.sub(
        r"\s+\d{2}(?:-?й)?\s*$",
        "",
        bare,
        flags=re.IGNORECASE,
    )

    bare = re.sub(
        r"\s*[-–—]?\s*(?:жылкы|жыл|года|год|г\.?)\s*$",
        "",
        bare,
        flags=re.IGNORECASE,
    )

    bare = re.sub(
        r"\s+",
        " ",
        bare,
    ).strip(" .,!?-")

    if _is_valid_car_model(bare):
        return bare

    return None


# ============================================================
# LOAN PROGRAM
# ============================================================

def _extract_loan_program(
    text: str,
) -> Optional[str]:

    lower = _clean_text(text).lower()

    if "автозалог" in lower:
        return "Автозалог"

    if "автозайм" in lower:
        return "Автозайм"

    # --------------------------------------------------------
    # CUSTOMER KEEPS VEHICLE
    # --------------------------------------------------------
    # "Без изъятия автомобиля" is the customer-retained
    # vehicle loan option. Internally this is treated as
    # the Автозайм program.
    # --------------------------------------------------------

    customer_vehicle_phrases = [

        # Short natural customer answers
        "нужен займ без изъятия",
        "хочу займ без изъятия",
        "займ без изъятия",
        "нужен без изъятия",
        "хочу без изъятия",

        # Normal Russian
        "без изъятия автомобиля",
        "без изъятия машины",
        "без передачи автомобиля",
        "без передачи машины",

        # Whisper / speech-recognition variants
        "без из яйти машины",
        "без из ятия машины",
        "без изъятия авто",
        "без из яйти авто",
        "без изъятия машин",
        "без передачи авто",
        "не изымать автомобиль",
        "не изымать машину",
        "машину не изымаем",
        "автомобиль не изымаем",
        "машина остается у нас",
        "машина останется у нас",
        "автомобиль остается у нас",
        "автомобиль останется у нас",
    ]

    for phrase in customer_vehicle_phrases:

        if phrase in lower:
            return "Автозайм"

    phrases = [

        "залог автомобиля",

        "автомобиль в качестве залога",

        "использовать его в качестве залога",

        "использовать автомобиль в качестве залога",

        "под залог автомобиля",

        "под залог машины",

        "машина в качестве залога",

        "автомобиль будет залогом",
    ]

    for phrase in phrases:

        if phrase in lower:
            return "Автозалог"

    return None


# ============================================================
# VEHICLE POSSESSION
# ============================================================

def _extract_vehicle_possession(
    text: str,
) -> Optional[str]:

    lower = _clean_text(text).lower()

    # --------------------------------------------------------
    # CUSTOMER KEEPS VEHICLE
    # --------------------------------------------------------

    customer_patterns = [

        # ----------------------------------------------------
        # KYRGYZ — CUSTOMER KEEPS VEHICLE
        # ----------------------------------------------------

        "машинаны өзүмдө калтыргым келет",
        "машинамды өзүмдө калтыргым келет",
        "унааны өзүмдө калтыргым келет",
        "унаамды өзүмдө калтыргым келет",

        "машина өзүмдө калсын",
        "машинам өзүмдө калсын",
        "унаа өзүмдө калсын",
        "унаам өзүмдө калсын",

        "машинаны өзүмдө калтырам",
        "машинамды өзүмдө калтырам",
        "унаамды өзүмдө калтырам",

        # Short natural customer answer
        "нужен займ без изъятия",
        "хочу займ без изъятия",
        "займ без изъятия",
        "нужен без изъятия",
        "хочу без изъятия",


        # Whisper / speech-recognition variants
        "без из яйти машины",
        "без изъятия авто",
        "без изъятия машин",
        "без изъятия транспортного средства",
        "без передачи авто",
        "не изымать автомобиль",
        "не изымать машину",
        "машину не изымаем",
        "автомобиль не изымаем",

        "без передачи автомобиля",

        "без изъятия автомобиля",

        "автомобиль останется у нас",

        "машина останется у нас",

        "автомобиль остается у нас",

        "машина остается у нас",

        "продолжим сами пользоваться автомобилем",

        "продолжим пользоваться автомобилем",

        "не будем передавать автомобиль",

        "не хотим оставлять автомобиль у вас",

        "без передачи машины",

        "без изъятия машины",

        "машина останется у меня",

        "автомобиль останется у меня",

        "автомобиль остается у меня",
    ]

    for phrase in customer_patterns:

        if phrase in lower:
            return "customer"

    # --------------------------------------------------------
    # LENDER TAKES VEHICLE
    # --------------------------------------------------------

    lender_patterns = [

        "с передачей автомобиля",

        "изъятие автомобиля",

        "на охраняемой стоянке",

        "оставить автомобиль у вас",

        "передать автомобиль вам",

        "передача автомобиля вам",

        "автомобиль будет у вас",

        "машина будет у вас",

        "передать машину вам",
    ]

    for phrase in lender_patterns:

        if phrase in lower:
            return "lender"

    return None


# ============================================================
# REGISTRATION REGION
# ============================================================

def _normalize_registration_region(
    value: Any,
) -> Optional[str]:

    if value is None:
        return None

    if not isinstance(value, str):
        return None

    value = _clean_text(value)

    if not value:
        return None

    value = value.strip(" .,!?;:")

    if not value:
        return None

    # --------------------------------------------------------
    # ONLY ACCEPT REAL KYRGYZSTAN REGIONS/CITIES
    # --------------------------------------------------------

    regions = {
        "бишкек": "Бишкек",
        "ош": "Ош",
        "чуй": "Чуй",
        "чуйская область": "Чуйская область",
        "ошская область": "Ошская область",
        "иссык-куль": "Иссык-Куль",
        "иссык куль": "Иссык-Куль",
        "иссык-кульская область": "Иссык-Кульская область",
        "нарын": "Нарын",
        "нарынская область": "Нарынская область",
        "талас": "Талас",
        "таласская область": "Таласская область",
        "джалал-абад": "Джалал-Абад",
        "джалал абад": "Джалал-Абад",
        "джалал-абадская область": "Джалал-Абадская область",
        "баткен": "Баткен",
        "баткенская область": "Баткенская область",
    }

    return regions.get(value.lower())


def _extract_registration_region(
    text: str,
) -> Optional[str]:

    text = _clean_text(text)

    # --------------------------------------------------------
    # NORMALIZED REGION MAP
    # --------------------------------------------------------

    regions = {
        # Bishkek
        "бишкек": "Бишкек",
        "бишкеке": "Бишкек",
        "бишкекте": "Бишкек",

        # Bosteri / Issyk-Kul
        # Bosteri is a settlement in the Issyk-Kul area.
        "бостери": "Иссык-Куль",
        "бостериде": "Иссык-Куль",
        "бостер": "Иссык-Куль",

        # Osh
        "ош": "Ош",
        "оше": "Ош",
        "ошто": "Ош",

        # Chuy
        "чуй": "Чуй",
        "чуйда": "Чуй",
        "чуйской": "Чуйская область",
        "чуйская область": "Чуйская область",

        # Osh region
        "ошская область": "Ошская область",

        # Issyk-Kul
        "иссык-куль": "Иссык-Куль",
        "иссык куль": "Иссык-Куль",
        "иссык-куле": "Иссык-Куль",
        "иссык-кульская область": "Иссык-Кульская область",

        # Naryn
        "нарын": "Нарын",
        "нарына": "Нарын",
        "нарында": "Нарын",
        "нарынская область": "Нарынская область",

        # Talas
        "талас": "Талас",
        "таласта": "Талас",
        "таласская область": "Таласская область",

        # Jalal-Abad
        "джалал-абад": "Джалал-Абад",
        "джалал абад": "Джалал-Абад",
        "джалал-абадда": "Джалал-Абад",
        "джалал-абадская область": "Джалал-Абадская область",

        # Batken
        "баткен": "Баткен",
        "баткенде": "Баткен",
        "баткенская область": "Баткенская область",
    }

    # --------------------------------------------------------
    # DIRECT REGION / CITY ANSWERS
    #
    # Customers often answer the question with only:
    #   Бишкек
    #   в Бишкеке
    #   Бостери
    #   в Бостери
    #
    # These must be recognized as registration_region before
    # generic extraction can mistake them for car_model.
    # --------------------------------------------------------

    direct_region = text.lower().strip(" .,!?;:")

    direct_region = re.sub(
        r"^(?:в|на)\s+",
        "",
        direct_region,
        flags=re.IGNORECASE,
    )

    normalized_direct = regions.get(direct_region)

    if normalized_direct:
        return normalized_direct

    # --------------------------------------------------------
    # KYRGYZ REGISTRATION
    #
    # Examples:
    #   Бишкекте катталгам
    #   Ошто катталгам
    #   Нарында катталгам
    #   Таласта катталгам
    #   Баткенде катталгам
    #   Чуйда катталгам
    # --------------------------------------------------------

    kyrgyz_patterns = [
        r"\b(бишкекте|ошто|нарында|таласта|баткенде|чуйда)\s+катталгам\b",
        r"\b(бишкекте|ошто|нарында|таласта|баткенде|чуйда)\s+катталганмын\b",
    ]

    for pattern in kyrgyz_patterns:
        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if match:
            raw = match.group(1).lower()
            normalized = regions.get(raw)

            if normalized:
                return normalized

    # --------------------------------------------------------
    # RUSSIAN REGISTRATION
    #
    # Examples:
    #   Я зарегистрирован в Бишкеке
    #   зарегистрирована в Бишкеке
    #   прописан в Оше
    # --------------------------------------------------------

    russian_patterns = [
        r"(?:я\s+)?"
        r"(?:зарегистрирован|"
        r"зарегистрирована|"
        r"зарегистрировано|"
        r"прописан|"
        r"прописана|"
        r"прописано)"
        r"\s+(?:в|на территории)\s+"
        r"([А-Яа-яЁёA-Za-z\- ]+?)"
        r"(?:[.!?,]|$)",

        r"(?:регистрация|"
        r"регион регистрации)"
        r"\s+(?:в|на территории)\s+"
        r"([А-Яа-яЁёA-Za-z\- ]+?)"
        r"(?:[.!?,]|$)",

        r"(?:регион|область|город)"
        r"\s*[:\-]\s*"
        r"([А-Яа-яЁёA-Za-z\- ]+?)"
        r"(?:[.!?,]|$)",
    ]

    for pattern in russian_patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if not match:
            continue

        raw = match.group(1).strip()

        raw = re.sub(
            r"\s+(?:и|но|поэтому|также|пожалуйста)\b.*$",
            "",
            raw,
            flags=re.IGNORECASE,
        ).strip()

        normalized = regions.get(raw.lower())

        if normalized:
            return normalized

    # --------------------------------------------------------
    # BARE REGION ANSWER
    # --------------------------------------------------------

    bare = text.strip().lower()

    return regions.get(bare)


# ============================================================
# MAIN DETERMINISTIC EXTRACTION
# ============================================================

def extract_fields(
    text: str,
) -> Dict[str, Any]:

    text = _clean_text(text)

    return {

        "car_model":
            _extract_car_model(text),

        "car_year":
            _extract_car_year(text),

        "car_value":
            _extract_car_value(text),

        "loan_amount":
            _extract_loan_amount(text),

        "loan_program":
            _extract_loan_program(text),

        "vehicle_possession":
            _extract_vehicle_possession(text),

        "registration_region":
            _extract_registration_region(text),

        "loan_term_months":
            _extract_loan_term(text),
    }


# ============================================================
# AI EXTRACTION VALIDATION
# ============================================================

def validate_extracted_field(
    field_name: str,
    value: Any,
) -> Any:

    if value is None:
        return None

    # --------------------------------------------------------
    # CAR MODEL
    # --------------------------------------------------------

    if field_name == "car_model":

        if not _is_valid_car_model(value):
            return None

        return _clean_text(value)

    # --------------------------------------------------------
    # LOAN PROGRAM
    # --------------------------------------------------------

    if field_name == "loan_program":

        if not isinstance(value, str):
            return None

        value = value.strip().lower()

        if value == "автозалог":
            return "Автозалог"

        if value == "автозайм":
            return "Автозайм"

        return None

    # --------------------------------------------------------
    # VEHICLE POSSESSION
    # --------------------------------------------------------

    if field_name == "vehicle_possession":

        if not isinstance(value, str):
            return None

        value = value.strip().lower()

        if value in {
            "customer",
            "клиент",
            "у клиента",
            "у заемщика",
            "у заёмщика",
        }:
            return "customer"

        if value in {
            "lender",
            "кредитор",
            "у кредитора",
        }:
            return "lender"

        return None

    # --------------------------------------------------------
    # REGISTRATION REGION
    # --------------------------------------------------------

    if field_name == "registration_region":

        if not isinstance(value, str):
            return None

        value = _normalize_registration_region(value)

        if not value:
            return None

        allowed_regions = {
            "бишкек",
            "ош",
            "чуй",
            "чуйская область",
            "ошская область",
            "иссык-куль",
            "иссык куль",
            "иссык-кульская область",
            "нарын",
            "нарынская область",
            "талас",
            "таласская область",
            "джалал-абад",
            "джалал абад",
            "джалал-абадская область",
            "баткен",
            "баткенская область",
        }

        if value.lower() not in allowed_regions:
            return None

        return value

    # --------------------------------------------------------
    # YEAR
    # --------------------------------------------------------

    if field_name == "car_year":

        try:
            year = int(value)
        except (TypeError, ValueError):
            return None

        if 1980 <= year <= 2035:
            return year

        return None

    # --------------------------------------------------------
    # LOAN TERM
    # --------------------------------------------------------

    if field_name == "loan_term_months":

        try:
            months = int(value)
        except (TypeError, ValueError):
            return None

        if 1 <= months <= 120:
            return months

        return None

    # --------------------------------------------------------
    # MONEY
    # --------------------------------------------------------

    if field_name in {
        "car_value",
        "loan_amount",
    }:

        if isinstance(value, str):

            normalized = _normalize_number(
                value
            )

        else:

            try:
                normalized = float(value)
            except (TypeError, ValueError):
                return None

        if normalized is None:
            return None

        if normalized <= 0:
            return None

        return normalized

    return value


# ============================================================
# SANITIZE AI EXTRACTION
# ============================================================

def sanitize_ai_extraction(
    extracted: Optional[Dict[str, Any]],
) -> Dict[str, Any]:

    if not isinstance(extracted, dict):
        return {}

    cleaned: Dict[str, Any] = {}

    for field_name in FIELDS:

        if field_name not in extracted:
            continue

        value = validate_extracted_field(
            field_name,
            extracted.get(field_name),
        )

        if value is not None:
            cleaned[field_name] = value

    return cleaned


# ============================================================
# MERGE EXTRACTION
# ============================================================

def merge_extraction(
    existing: Dict[str, Any],
    extracted: Dict[str, Any],
) -> Dict[str, Any]:

    merged = dict(existing)

    extracted = sanitize_ai_extraction(
        extracted
    )

    for field_name in FIELDS:

        new_value = extracted.get(
            field_name
        )

        if new_value is None:
            continue

        if (
            isinstance(new_value, str)
            and not new_value.strip()
        ):
            continue

        merged[field_name] = new_value

    return merged


# ============================================================
# DETERMINISTIC-FIRST MERGE
# ============================================================

def merge_deterministic_over_ai(
    ai_extracted: Optional[Dict[str, Any]],
    deterministic_extracted: Optional[Dict[str, Any]],
) -> Dict[str, Any]:

    ai_clean = sanitize_ai_extraction(
        ai_extracted or {}
    )

    deterministic_clean = sanitize_ai_extraction(
        deterministic_extracted or {}
    )

    final: Dict[str, Any] = {}

    for field_name in FIELDS:

        deterministic_value = (
            deterministic_clean.get(
                field_name
            )
        )

        ai_value = (
            ai_clean.get(
                field_name
            )
        )

        # ----------------------------------------------------
        # DETERMINISTIC ALWAYS WINS
        # ----------------------------------------------------

        if deterministic_value is not None:

            final[field_name] = (
                deterministic_value
            )

        elif ai_value is not None:

            final[field_name] = ai_value

        else:

            final[field_name] = None

    return final


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

extract_information = extract_fields

extract_customer_fields = extract_fields


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    tests = [

        "400 000 сом.",

        "Я хочу получить 600 000 сом.",

        "Тогда я хочу получить 100 000 сом.",

        "Мы хотели бы получить под него 400 000 сом.",

        "Нам нужно 400 000 сом на один месяц.",

        "Примерная стоимость автомобиля 1 500 000 сом.",

        "Это BYD Song Plus.",

        "2024 года.",

        "Автозалог, без передачи автомобиля.",

        "Я зарегистрирована в Бишкеке.",
    ]

    print("=" * 70)
    print("DETERMINISTIC EXTRACTION TEST")
    print("=" * 70)

    for index, text in enumerate(
        tests,
        start=1,
    ):

        print()
        print(f"TEST {index}")
        print("INPUT:", text)
        print("OUTPUT:")
        print(extract_fields(text))

    # ========================================================
    # FULL CONVERSATION TEST
    # ========================================================

    print()
    print("=" * 70)
    print("FULL CONVERSATION TEST")
    print("=" * 70)

    test = """

    Здравствуйте. Я вчера вам звонила по поводу автомобиля.

    Мы хотели бы использовать его в качестве залога.

    Мы хотели бы получить под него 400 000 сом.

    Пожалуйста, рассчитайте сумму 400 000 сом
    без передачи автомобиля.

    Нам нужно 400 000 сом на один месяц.

    Это BYD Song Plus, 2024 года.

    Примерная стоимость автомобиля
    1 500 000 сом.

    Автозалог, но без передачи автомобиля.

    Я зарегистрирована в Бишкеке.
    """

    result = extract_fields(test)

    print()
    print("DETERMINISTIC RESULT:")
    print(result)

    # ========================================================
    # FAKE AI RESULT
    # ========================================================

    fake_ai = {
        "car_model": "возможно",
        "car_year": None,
        "car_value": None,
        "loan_amount": 400000,
        "loan_program": None,
        "vehicle_possession": None,
        "registration_region": None,
        "loan_term_months": None,
    }

    final = merge_deterministic_over_ai(
        fake_ai,
        result,
    )

    print()
    print("AI RESULT:")
    print(fake_ai)

    print()
    print("FINAL MERGED RESULT:")
    print(final)

    # ========================================================
    # EXPECTED IMPORTANT VALUES
    # ========================================================

    print()
    print("=" * 70)
    print("EXPECTED IMPORTANT VALUES")
    print("=" * 70)

    print("car_model:", result["car_model"])
    print("car_year:", result["car_year"])
    print("car_value:", result["car_value"])
    print("loan_amount:", result["loan_amount"])
    print("loan_program:", result["loan_program"])
    print("vehicle_possession:", result["vehicle_possession"])
    print("registration_region:", result["registration_region"])
    print("loan_term_months:", result["loan_term_months"])

    # ========================================================
    # AUTOMATIC CHECKS
    # ========================================================

    print()
    print("=" * 70)
    print("AUTOMATIC CHECKS")
    print("=" * 70)

    expected = {
        "car_model": "BYD Song Plus",
        "car_year": 2024,
        "car_value": 1500000.0,
        "loan_amount": 400000.0,
        "loan_program": "Автозалог",
        "vehicle_possession": "customer",
        "registration_region": "Бишкеке",
        "loan_term_months": 1,
    }

    all_passed = True

    for field_name, expected_value in expected.items():

        actual_value = final.get(
            field_name
        )

        passed = actual_value == expected_value

        print(
            f"{field_name}: "
            f"{'PASS' if passed else 'FAIL'} "
            f"| expected={expected_value!r} "
            f"| actual={actual_value!r}"
        )

        if not passed:
            all_passed = False

    print()

    if all_passed:
        print("ALL CHECKS PASSED")
    else:
        print("SOME CHECKS FAILED")
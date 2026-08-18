import re


# ============================================================
# EMPTY INFORMATION
# ============================================================

def empty_information():
    return {
        "car_model": None,
        "car_year": None,
        "car_value": None,
        "loan_amount": None,
        "loan_program": None,
        "vehicle_possession": None,
        "registration_region": None,
        "loan_term_months": None,
    }


# ============================================================
# NUMBER NORMALIZATION
# ============================================================

def parse_number(value):
    if value is None:
        return None

    value = str(value).strip().lower()

    value = value.replace("\u00a0", " ")

    # Detect Russian and Kyrgyz numeric multipliers.
    multiplier = 1

    if re.search(
        r"\b(?:млн|миллион(?:а|ов)?|миллиард(?:а|ов)?)\b",
        value
    ):
        if re.search(
            r"\b(?:миллиард(?:а|ов)?)\b",
            value
        ):
            multiplier = 1_000_000_000
        else:
            multiplier = 1_000_000

    elif re.search(
        r"\b(?:тыс|тысяч|тысяча|миң|мин)\b",
        value
    ):
        multiplier = 1_000

    elif re.search(
        r"(?:\bк\b|(?<=\d)к\b)",
        value
    ):
        multiplier = 1_000

    # Keep only the numeric portion.
    number_match = re.search(
        r"\d[\d\s]*(?:[.,]\d+)?",
        value
    )

    if not number_match:
        return None

    number = number_match.group(0)
    number = number.replace(" ", "")

    try:
        if "," in number and "." in number:
            number = number.replace(",", "")

        elif "," in number:
            parts = number.split(",")

            if len(parts) == 2 and len(parts[1]) <= 2:
                number = number.replace(",", ".")
            else:
                number = number.replace(",", "")

        result = float(number) * multiplier

        return result

    except (TypeError, ValueError):
        return None


# ============================================================
# MONEY REGEX
# ============================================================

MONEY_PATTERN = (
    r"(\d[\d\s\u00a0]*(?:[.,]\d+)?"
    r"\s*(?:(?:млн|миллион(?:а|ов)?|тыс|тысяч|тысяча|к)"
    r"\s*)?"
    r"(?:сом|сомов|сома|с)\b)"
)


def find_money_values(text):
    values = []

    for match in re.finditer(
        MONEY_PATTERN,
        text,
        flags=re.IGNORECASE
    ):
        number = parse_number(match.group(1))

        if number is not None:
            values.append(number)

    return values


# ============================================================
# LOAN AMOUNT
# ============================================================

def extract_loan_amount(text):

    patterns = [

        # ========================================================
        # RUSSIAN
        # ========================================================

        # Мне нужно примерно 500 тысяч сом
        r"\bмне\s+нужн[оа]\s+"
        r"(?:примерно\s+|около\s+|приблизительно\s+)?"
        + MONEY_PATTERN,

        # Мне нужен займ примерно 500 тысяч сом
        r"\bмне\s+нужен\s+займ\s+"
        r"(?:примерно\s+|около\s+|приблизительно\s+)?"
        + MONEY_PATTERN,

        # Нам нужно 500 тысяч сом
        r"\bнам\s+нужн[оа]\s+"
        r"(?:примерно\s+|около\s+|приблизительно\s+)?"
        + MONEY_PATTERN,

        # Хотим получить 500000 сом
        r"\b(?:мы\s+)?хотим\s+получить\s+"
        + MONEY_PATTERN,

        # Хотели бы получить 500000 сом
        r"\bхотели\s+бы\s+получить\s+"
        + MONEY_PATTERN,

        # Хочу получить / взять 500000 сом
        r"\b(?:хочу|хотим)\s+(?:получить|взять)\s+"
        + MONEY_PATTERN,

        # Хочу взять 500к / 500 тысяч / 500 тыс
        # Russian shorthand without the word "сом"
        r"\b(?:хочу|хотим)\s+(?:получить|взять)\s+"
        r"(\d+(?:[.,]\d+)?\s*"
        r"(?:млн|миллион(?:а|ов)?|тыс|тысяч|тысяча|к))\b",

        # Получить под него 500000 сом
        r"\bполучить\s+под\s+(?:него|этот\s+автомобиль)\s+"
        + MONEY_PATTERN,

        # Сумма 500000 сом
        r"\bсумм[ау]\s+"
        + MONEY_PATTERN,

        # Займ 500000 сом
        r"\bзайм(?:а)?\s+"
        + MONEY_PATTERN,


        # ========================================================
        # KYRGYZ
        # ========================================================

        # 500 миң сом алгым келет
        # 500 мин сом алгым келет
        # 500к сом алгым келет
        r"\b"
        r"(\d[\d\s\u00a0]*(?:[.,]\d+)?"
        r"\s*(?:(?:миң|мин|тыш|млн|миллион(?:а|ов)?|к)\s*)?)"
        r"\s*(?:сом|сомов|сома|с)\b"
        r".{0,40}?"
        r"\bалгым\s+келет\b",

        # 500 миң сом алгым
        r"\b"
        r"(\d[\d\s\u00a0]*(?:[.,]\d+)?"
        r"\s*(?:(?:миң|мин|тыш|млн|миллион(?:а|ов)?|к)\s*)?)"
        r"\s*(?:сом|сомов|сома|с)\b"
        r".{0,40}?"
        r"\bалгым\b",

        # Насыя катары 500 миң сом алгым келет
        r"\bнасыя"
        r".{0,80}?"
        r"(\d[\d\s\u00a0]*(?:[.,]\d+)?"
        r"\s*(?:(?:миң|мин|тыш|млн|миллион(?:а|ов)?|к)\s*)?)"
        r"\s*(?:сом|сомов|сома|с)\b",

        # 500 миң сом керек
        r"\b"
        r"(\d[\d\s\u00a0]*(?:[.,]\d+)?"
        r"\s*(?:(?:миң|мин|тыш|млн|миллион(?:а|ов)?|к)\s*)?)"
        r"\s*(?:сом|сомов|сома|с)\b"
        r".{0,30}?"
        r"\bкерек\b",

        # Мага 500 миң сом керек
        r"\bмага\s+"
        r"(\d[\d\s\u00a0]*(?:[.,]\d+)?"
        r"\s*(?:(?:миң|мин|тыш|млн|миллион(?:а|ов)?|к)\s*)?)"
        r"\s*(?:сом|сомов|сома|с)\b"
        r".{0,30}?"
        r"\bкерек\b",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE | re.DOTALL
        )

        if not match:
            continue

        for group in match.groups():

            number = parse_number(group)

            if number is not None:

                if 1_000 <= number <= 100_000_000:
                    return number

    return None


# ============================================================
# CAR YEAR
# ============================================================

def extract_car_year(text):

    patterns = [

        # --------------------------------------------------------
        # RUSSIAN
        # --------------------------------------------------------

        # 2021 года / 2021 год / 2021 г.
        r"\b(19\d{2}|20\d{2})\s*(?:года|год|г\.)?\b",

        # 21 года / 21 год / 21 г.
        r"\b(\d{2})\s*(?:года|год|г\.)\b",

        # --------------------------------------------------------
        # KYRGYZ
        # --------------------------------------------------------

        # 2021-жылы / 2021-жылы
        r"\b(19\d{2}|20\d{2})\s*-\s*жылы\b",

        # 2021-жыл / 2021 жыл
        r"\b(19\d{2}|20\d{2})\s*-\s*жыл(?:ы)?\b",

        # 21-жылы / 21-жылы
        r"\b(\d{2})\s*-\s*жылы\b",

        # 21-жыл / 21 жыл
        r"\b(\d{2})\s*-\s*жыл(?:ы)?\b",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        if not match:
            continue

        raw_year = match.group(1)
        value = int(raw_year)

        if len(raw_year) == 2:
            year = 2000 + value
        else:
            year = value

        if 1950 <= year <= 2035:
            return year

    return None


# ============================================================
# CLEAN CAR MODEL
# ============================================================

def clean_car_model(value):

    if not value:
        return None

    value = value.strip()

    # Remove punctuation
    value = re.sub(
        r"[.!?,:;]+$",
        "",
        value
    ).strip()

    # Remove year from model
    value = re.sub(
        r"\b(19\d{2}|20\d{2})\s*"
        r"(?:года|год|г\.)?\b",
        "",
        value,
        flags=re.IGNORECASE
    ).strip()

    # Remove common connecting words
    value = re.sub(
        r"\s+(?:года|год|г\.)$",
        "",
        value,
        flags=re.IGNORECASE
    ).strip()

    # Remove excessive spaces
    value = re.sub(
        r"\s+",
        " ",
        value
    ).strip()

    if not value:
        return None

    return value


# ============================================================
# CAR MODEL
# ============================================================

def extract_car_model(text):

    # --------------------------------------------------------
    # Explicit model after "это"
    # --------------------------------------------------------

    patterns = [

        r"\bэто\s+"
        r"([A-Za-zА-Яа-яЁё0-9][A-Za-zА-Яа-яЁё0-9._-]*"
        r"(?:\s+[A-Za-zА-Яа-яЁё0-9._-]+){0,4})"
        r"(?:[.!?,]|$)",

        r"\bмарка\s+и\s+модель\s*[:\-]?\s*"
        r"([A-Za-zА-Яа-яЁё0-9][A-Za-zА-Яа-яЁё0-9._-]*"
        r"(?:\s+[A-Za-zА-Яа-яЁё0-9._-]+){0,4})"
        r"(?:[.!?,]|$)",

        r"\bмодель\s+автомобиля\s*[:\-]?\s*"
        r"([A-Za-zА-Яа-яЁё0-9][A-Za-zА-Яа-яЁё0-9._-]*"
        r"(?:\s+[A-Za-zА-Яа-яЁё0-9._-]+){0,4})"
        r"(?:[.!?,]|$)",
    ]

    forbidden_words = {
        "автомобиль",
        "машина",
        "новый",
        "новая",
        "новое",
        "современный",
        "этот",
    }

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        if not match:
            continue

        value = clean_car_model(
            match.group(1)
        )

        if not value:
            continue

        if value.lower() in forbidden_words:
            continue

        if 1 <= len(value.split()) <= 5:
            return value

    # --------------------------------------------------------
    # Common standalone models
    #
    # Customers often omit the manufacturer:
    # "камри 21 года"
    # "прадо 2020"
    # "солярис 2019 года"
    # --------------------------------------------------------

    known_models = [
        "камри",
        "camry",
        "прадо",
        "prado",
        "королла",
        "corolla",
        "рав4",
        "rav4",
        "солярис",
        "solaris",
        "акцент",
        "accent",
        "лансер",
        "lancer",
        "круз",
        "cruze",
        "нива",
        "niva",
        "патрол",
        "patrol",
        "лексус",
        "lexus",
        "джетта",
        "jetta",
        "пассат",
        "passat",
    ]

    for model in known_models:
        match = re.search(
            rf"\b{re.escape(model)}\b",
            text,
            flags=re.IGNORECASE
        )

        if match:
            return match.group(0)

    # --------------------------------------------------------
    # Known brands
    # --------------------------------------------------------

    known_brands = [
        "BYD",
        "Toyota",
        "Lexus",
        "BMW",
        "Mercedes-Benz",
        "Mercedes",
        "Hyundai",
        "Kia",
        "Honda",
        "Nissan",
        "Volkswagen",
        "Audi",
        "Tesla",
        "Geely",
        "Chery",
        "Haval",
        "Changan",
        "Ford",
        "Chevrolet",
    ]

    for brand in known_brands:

        pattern = (
            rf"\b{re.escape(brand)}"
            r"(?:\s+[A-Za-zА-Яа-яЁё0-9._-]+){1,4}"
        )

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        if not match:
            continue

        value = clean_car_model(
            match.group(0)
        )

        if not value:
            continue

        # Don't accidentally include loan/application words
        value = re.split(
            r"\b(?:хочу|хотим|нужн[оа]|получить|займ|"
            r"стоимость|цена|под|автозалог|автозайм)\b",
            value,
            maxsplit=1,
            flags=re.IGNORECASE
        )[0].strip()

        value = clean_car_model(value)

        if value and len(value.split()) <= 5:
            return value

    return None


# ============================================================
# CAR VALUE
# ============================================================

def extract_car_value(text):

    text = text.strip()

    # --------------------------------------------------------
    # Explicit car-value patterns
    # --------------------------------------------------------

    patterns = [

        # --------------------------------------------------------
        # RUSSIAN — messy car-value wording
        # --------------------------------------------------------

        # Думаю, она где-то 1.5 млн стоит
        r"\b(?:думаю|кажется|примерно|полагаю)"
        r".{0,40}?"
        r"(\d+(?:[.,]\d+)?\s*(?:млн|миллион(?:а|ов)?|тыс|тысяч|тысяча|к))"
        r"\s*(?:сом|сома|сомов)?"
        r".{0,20}?\bстоит\b",

        # Она где-то 1.5 млн стоит
        r"\b(?:она|он|машина|автомобиль)"
        r".{0,30}?"
        r"(\d+(?:[.,]\d+)?\s*(?:млн|миллион(?:а|ов)?|тыс|тысяч|тысяча|к))"
        r"\s*(?:сом|сома|сомов)?"
        r".{0,20}?\bстоит\b",

        # --------------------------------------------------------
        # KYRGYZ — messy car-value wording
        # --------------------------------------------------------

        # Унаам болжол менен 1.5 млн сом турат
        r"\b(?:унаам|унаа|машинам)"
        r".{0,40}?"
        r"(\d+(?:[.,]\d+)?\s*(?:млн|миллион|миң|мин|к))"
        r"\s*(?:сом|сома|сомов)?"
        r".{0,30}?\bтурат\b",

        # 1.5 млн сом турат
        r"\b"
        r"(\d+(?:[.,]\d+)?\s*(?:млн|миллион|миң|мин|к))"
        r"\s*(?:сом|сома|сомов)?"
        r".{0,30}?\bтурат\b",

        # 1500000 сом турат
        r"\b"
        r"(\d[\d\s\u00a0]*(?:[.,]\d+)?)"
        r"\s*(?:сом|сома|сомов)"
        r".{0,30}?\bтурат\b",


        # Машина стоит примерно 1500000 сом
        r"\b(?:автомобиль|машина)\s+"
        r"(?:стоит|обойдется|обойдётся)"
        r"(?:\s+примерно|\s+около|\s+приблизительно)?\s*"
        + MONEY_PATTERN,

        # Стоимость автомобиля 1500000 сом
        r"\b(?:примерная\s+)?стоимость\s+"
        r"(?:автомобиля|машины)"
        r".{0,100}?"
        + MONEY_PATTERN,

        # Думаю, ее стоимость около 1.5 млн сом
        r"\b(?:е[её]|его|машины|автомобиля)\s+"
        r"стоимость\s+"
        r"(?:примерно|около|приблизительно)?\s*"
        r"(" + r"\d+(?:[.,]\d+)?\s*(?:млн|миллион(?:а|ов)?|тыс|тысяч|к)" + r")"
        r"\s*(?:сом|сома|сомов)?\b",

        # Стоимость около 1.5 млн сом
        r"\bстоимость\s+"
        r"(?:примерно|около|приблизительно)?\s*"
        r"(" + r"\d+(?:[.,]\d+)?\s*(?:млн|миллион(?:а|ов)?|тыс|тысяч|к)" + r")"
        r"\s*(?:сом|сома|сомов)?\b",

        # Цена около 1.5 млн сом
        r"\bцена\s+"
        r"(?:примерно|около|приблизительно)?\s*"
        r"(" + r"\d+(?:[.,]\d+)?\s*(?:млн|миллион(?:а|ов)?|тыс|тысяч|к)" + r")"
        r"\s*(?:сом|сома|сомов)?\b",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        if not match:
            continue

        value = parse_number(
            match.group(1) if match.lastindex else match.group(0)
        )

        if value is not None and value > 0:
            return value

    # --------------------------------------------------------
    # IMPORTANT:
    # Do NOT use generic money phrases here.
    #
    # Example:
    # "Мне нужно примерно 500 тысяч сом."
    #
    # is a loan request, not a car value.
    # --------------------------------------------------------

    return None


# ============================================================
# LOAN PROGRAM
# ============================================================

def extract_loan_program(text):

    text_lower = text.lower().strip()

    # --------------------------------------------------------
    # VEHICLE POSSESSION PHRASES ARE NOT LOAN PROGRAMS
    #
    # These phrases describe whether the customer keeps
    # the vehicle. That information belongs to
    # vehicle_possession, not loan_program.
    # --------------------------------------------------------

    customer_possession_patterns = [
        "без изъятия автомобиля",
        "без изъятия машины",
        "без передачи автомобиля",
        "без передачи машины",
        "автомобиль останется у меня",
        "машина останется у меня",
    ]

    for phrase in customer_possession_patterns:
        if phrase in text_lower:
            return None

    lender_possession_patterns = [
        "с размещением автомобиля",
        "с размещением машины",
        "с передачей автомобиля",
        "с передачей машины",
        "на охраняемой стоянке",
        "на стоянке",
    ]

    for phrase in lender_possession_patterns:
        if phrase in text_lower:
            return None

    # --------------------------------------------------------
    # OTHER PROGRAM NAMES
    # --------------------------------------------------------

    if "автозалог" in text_lower:
        return "Автозалог"

    if "автозайм" in text_lower:
        return "Автозайм"

    return None


# ============================================================
# VEHICLE POSSESSION
# ===========================================================
def extract_vehicle_possession(text):

    text_lower = text.lower().strip()

    # --------------------------------------------------------
    # CUSTOMER KEEPS VEHICLE
    # --------------------------------------------------------

    customer_patterns = [

        # Russian
        "без передачи автомобиля",
        "без передачи машины",
        "без изъятия автомобиля",
        "без изъятия машины",
        "автомобиль останется у меня",
        "машина останется у меня",
        "автомобиль остается у меня",
        "машина остается у меня",
        "автомобиль останется у клиента",
        "машина останется у клиента",
        "оставить автомобиль у себя",
        "оставить машину у себя",
        "машину хочу оставить у себя",
        "автомобиль хочу оставить у себя",
        "хочу оставить машину у себя",
        "хочу оставить автомобиль у себя",
        "машина будет у меня",
        "автомобиль будет у меня",
        "машину оставлю у себя",
        "автомобиль оставлю у себя",
        "без передачи",

        # Kyrgyz
        "унаа өзүмдө калсын",
        "унаам өзүмдө калсын",
        "унаа өзүмдө калат",
        "унаам өзүмдө калат",
        "унааны өзүмдө калтыр",
        "унаамды өзүмдө калтыр",
        "унаа менде калсын",
        "унаам менде калсын",
        "унаа менде калат",
        "унаам менде калат",
    ]

    for phrase in customer_patterns:

        if phrase in text_lower:
            return "customer"

    # --------------------------------------------------------
    # VEHICLE TRANSFERRED / SECURED PARKING
    # --------------------------------------------------------

    lender_patterns = [

        # Russian
        "с передачей автомобиля",
        "с передачей машины",
        "передать автомобиль",
        "передать машину",
        "автомобиль передается",
        "машина передается",
        "с размещением автомобиля",
        "с размещением машины",
        "на охраняемой стоянке",
        "на стоянке",
        "автомобиль будет на стоянке",
        "машина будет на стоянке",

        # Kyrgyz
        "унааны өткөрүп берем",
        "унаамды өткөрүп берем",
        "унаа өткөрүлөт",
        "унаам өткөрүлөт",
        "унаа токтотуучу жайда болот",
        "унаам токтотуучу жайда болот",
        "унаа унаа токтотуучу жайда",
        "кайтарылуучу жайда",
    ]

    for phrase in lender_patterns:

        if phrase in text_lower:
            return "lender"

    return None


# ============================================================
# REGISTRATION REGION
# ============================================================
def extract_registration_region(text):

    text_clean = text.strip()
    text_lower = text_clean.lower()

    # --------------------------------------------------------
    # Russian
    # --------------------------------------------------------

    patterns = [

        r"\bя\s+зарегистрирован[аы]?\s+в\s+"
        r"([А-Яа-яЁёA-Za-z -]+)",

        r"\bзарегистрирован[аы]?\s+в\s+"
        r"([А-Яа-яЁёA-Za-z -]+)",

        r"\bрегистрация\s+"
        r"(?:в|:)\s*"
        r"([А-Яа-яЁёA-Za-z -]+)",

        # Kyrgyz
        r"^(.+?)\s+катталганмын[.!?]?$",

        r"^(.+?)\s+катталгам[.!?]?$",

        r"^мен\s+(.+?)\s+катталганмын[.!?]?$",

        r"^мен\s+(.+?)\s+катталгам[.!?]?$",
    ]

    known_regions = {

        "бишкек": "Бишкек",
        "бишкекте": "Бишкек",

        "ош": "Ош",
        "ошто": "Ош",

        "чуй": "Чуй",
        "чуйда": "Чуй",

        "ошская область": "Ошская область",

        "иссык-куль": "Иссык-Куль",
        "иссык куль": "Иссык-Куль",

        "нарын": "Нарын",
        "нарында": "Нарын",

        "талас": "Талас",
        "таласта": "Талас",

        "джалал-абад": "Джалал-Абад",
        "джалал абад": "Джалал-Абад",

        "баткен": "Баткен",
        "баткенде": "Баткен",
    }

    for pattern in patterns:

        match = re.search(
            pattern,
            text_clean,
            flags=re.IGNORECASE
        )

        if not match:
            continue

        value = match.group(1).strip()

        value = re.sub(
            r"[.!?,:;]+$",
            "",
            value
        ).strip()

        value = re.sub(
            r"^(мен\s+)",
            "",
            value,
            flags=re.IGNORECASE
        ).strip()

        if not value:
            continue

        normalized = value.lower().strip()

        if normalized in known_regions:
            return known_regions[normalized]

        # Remove Russian locative endings for known cities.
        if normalized.endswith("е"):
            candidate = normalized[:-1]
            if candidate in known_regions:
                return known_regions[candidate]

        return value

    # --------------------------------------------------------
    # Simple known-region answer
    # --------------------------------------------------------

    normalized = text_lower.strip()

    return known_regions.get(normalized)


# ============================================================
# LOAN TERM
# ============================================================

def extract_loan_term(text):

    patterns = [

        # Russian
        r"\bна\s+(\d+)\s*"
        r"(?:месяц|месяца|месяцев|мес\.?)\b",

        r"\bсрок(?:ом)?\s+"
        r"(\d+)\s*"
        r"(?:месяц|месяца|месяцев|мес\.?)\b",

        # Kyrgyz:
        # 24 айга алгым келет
        r"\b(\d+)\s*"
        r"(?:айга|ай)\b",

        # 24 ай мөөнөткө
        r"\b(\d+)\s*"
        r"(?:айлык|ай)\s+"
        r"(?:мөөнөткө|мөөнөт)",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        if not match:
            continue

        months = int(match.group(1))

        if 1 <= months <= 120:
            return months

    return None


# ============================================================
# MAIN EXTRACTOR
# ============================================================

def extract_information_with_ai(message):

    information = empty_information()

    if not message:
        return information

    text = message.strip()

    information["car_model"] = extract_car_model(text)

    information["car_year"] = extract_car_year(text)

    information["car_value"] = extract_car_value(text)

    information["loan_amount"] = extract_loan_amount(text)

    information["loan_program"] = extract_loan_program(text)

    information["vehicle_possession"] = (
        extract_vehicle_possession(text)
    )

    information["registration_region"] = (
        extract_registration_region(text)
    )

    information["loan_term_months"] = (
        extract_loan_term(text)
    )

    return information


# ============================================================
# COMPATIBILITY ALIAS
# ============================================================

extract_information = extract_information_with_ai

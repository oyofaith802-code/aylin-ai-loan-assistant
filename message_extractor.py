import re


def _parse_amount(value: str) -> float | None:
    """
    Convert a number such as:
    500000
    500 000
    1,200,000
    into a float.
    """

    value = value.replace(" ", "")
    value = value.replace(",", "")

    try:
        return float(value)
    except ValueError:
        return None


def extract_customer_information(message: str) -> dict:
    """
    Extract customer information using deterministic rules.

    Important:
    Monetary amounts are classified according to
    the words surrounding the amount.
    """

    information = {}

    message_lower = message.lower()

    # ---------------------------------------------------------
    # Car year
    # ---------------------------------------------------------

    year_match = re.search(
        r"\b(19\d{2}|20\d{2})\b",
        message
    )

    if year_match:
        information["car_year"] = int(
            year_match.group(1)
        )

    # ---------------------------------------------------------
    # Car value
    # ---------------------------------------------------------

    car_value_patterns = [
        r"(?:машина|автомобиль|авто).*?"
        r"(?:стоит|стоимость|цена)"
        r".*?"
        r"(\d[\d\s,.]*)\s*(?:сом|сомов|сомони)\b",

        r"(?:стоимость|цена)"
        r".*?"
        r"(\d[\d\s,.]*)\s*(?:сом|сомов|сомони)\b",
    ]

    for pattern in car_value_patterns:

        match = re.search(
            pattern,
            message_lower
        )

        if match:
            amount = _parse_amount(
                match.group(1)
            )

            if amount is not None:
                information["car_value"] = amount
                break

    # ---------------------------------------------------------
    # Loan amount
    # ---------------------------------------------------------

    loan_amount_patterns = [
        r"(?:хочу|нужно|нужен|нужна|получить|получу)"
        r".*?"
        r"(\d[\d\s,.]*)\s*(?:сом|сомов|сомони)\b",

        r"(?:сумма займа|сумму займа|размер займа)"
        r".*?"
        r"(\d[\d\s,.]*)\s*(?:сом|сомов|сомони)\b",

        r"(?:займ|заём)"
        r".*?"
        r"(\d[\d\s,.]*)\s*(?:сом|сомов|сомони)\b",
    ]

    for pattern in loan_amount_patterns:

        match = re.search(
            pattern,
            message_lower
        )

        if match:
            amount = _parse_amount(
                match.group(1)
            )

            if amount is not None:
                information["loan_amount"] = amount
                break

    # ---------------------------------------------------------
    # Car model
    # ---------------------------------------------------------

    car_models = [
        "Toyota Camry",
        "Toyota Corolla",
        "Honda Civic",
        "Honda CR-V",
        "Lexus RX",
        "BMW",
        "Mercedes"
    ]

    for model in car_models:

        if model.lower() in message_lower:
            information["car_model"] = model
            break

    # ---------------------------------------------------------
    # Loan program
    # ---------------------------------------------------------

    loan_programs = {
        "автозалог": "Автозалог",
        "автозайм": "Автозайм",
        "залог автомобиля": "Автозалог",
        "займ под залог автомобиля": "Автозалог"
    }

    for phrase, program in loan_programs.items():

        if phrase in message_lower:
            information["loan_program"] = program
            break

    # ---------------------------------------------------------
    # Registration region
    # ---------------------------------------------------------

    regions = {
        "бишкек": "Бишкек",
        "ош": "Ош",
        "джалал-абад": "Джалал-Абад",
        "жалал-абад": "Джалал-Абад",
        "каракол": "Каракол",
        "токмок": "Токмок"
    }

    for region, normalized_region in regions.items():

        if region in message_lower:
            information["registration_region"] = normalized_region
            break

    return information
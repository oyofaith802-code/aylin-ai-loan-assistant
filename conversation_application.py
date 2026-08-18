from __future__ import annotations

import re

from customer_card import CustomerCard

from ai_extractor import (
    extract_information_with_ai
)

from extraction import (
    extract_fields as extract_deterministic_fields
)

from decision_engine import (
    evaluate_application
)


# ============================================================
# EMPTY INFORMATION
# ============================================================

def empty_information():

    return {
        "car_model": None,
        "car_year": None,
        "car_value": None,

        "loan_amounts": [],
        "loan_amount": None,

        "loan_program": None,
        "vehicle_possession": None,
        "registration_region": None,
        "loan_term_months": None,
    }


# ============================================================
# NORMALIZE NUMBER
# ============================================================

def normalize_number(value):

    if value is None:
        return None

    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).strip()

    if not text:
        return None

    text = text.replace("\xa0", " ")

    # 400 000
    if re.fullmatch(
        r"\d{1,3}(?:\s\d{3})+",
        text,
    ):
        return float(text.replace(" ", ""))

    # 400,000
    if re.fullmatch(
        r"\d{1,3}(?:,\d{3})+",
        text,
    ):
        return float(text.replace(",", ""))

    # 400.000
    if re.fullmatch(
        r"\d{1,3}(?:\.\d{3})+",
        text,
    ):
        return float(text.replace(".", ""))

    try:
        return float(text.replace(",", "."))

    except (TypeError, ValueError):
        return None


# ============================================================
# NORMALIZE INFORMATION
# ============================================================

def normalize_information(information):

    if not isinstance(information, dict):
        return empty_information()

    normalized = empty_information()

    # ---------------------------------------------------------
    # SIMPLE FIELDS
    # ---------------------------------------------------------

    for field in (
        "car_model",
        "car_year",
        "car_value",
        "loan_program",
        "vehicle_possession",
        "registration_region",
        "loan_term_months",
    ):

        value = information.get(field)

        if value is not None:

            if isinstance(value, str):

                value = value.strip()

                if not value:
                    continue

            # -------------------------------------------------
            # NORMALIZE REGISTRATION REGION
            # -------------------------------------------------

            if field == "registration_region":

                region_map = {
                    "бишкек": "Бишкек",
                    "бишкеке": "Бишкек",

                    "ош": "Ош",
                    "оше": "Ош",

                    "чуй": "Чуй",
                    "чуе": "Чуй",
                    "чуйская область": "Чуйская область",

                    "ошская область": "Ошская область",

                    "иссык-куль": "Иссык-Куль",
                    "иссык куль": "Иссык-Куль",
                    "иссык-куле": "Иссык-Куль",
                    "иссык-кульская область": "Иссык-Кульская область",

                    "нарын": "Нарын",
                    "нарыне": "Нарын",
                    "нарынская область": "Нарынская область",

                    "талас": "Талас",
                    "таласе": "Талас",
                    "таласская область": "Таласская область",

                    "джалал-абад": "Джалал-Абад",
                    "джалал абад": "Джалал-Абад",
                    "джалал-абаде": "Джалал-Абад",
                    "джалал-абадская область": "Джалал-Абадская область",

                    "баткен": "Баткен",
                    "баткене": "Баткен",
                    "баткенская область": "Баткенская область",
                }

                value = region_map.get(
                    value.lower(),
                    value
                )

            normalized[field] = value

    # ---------------------------------------------------------
    # LOAN AMOUNT
    # ---------------------------------------------------------

    direct_amount = normalize_number(
        information.get("loan_amount")
    )

    if direct_amount is not None and direct_amount > 0:

        normalized["loan_amount"] = direct_amount

        normalized["loan_amounts"].append(
            direct_amount
        )

    # ---------------------------------------------------------
    # LOAN AMOUNTS LIST
    # ---------------------------------------------------------

    amounts = information.get(
        "loan_amounts",
        []
    )

    if isinstance(amounts, (list, tuple)):

        for amount in amounts:

            value = normalize_number(amount)

            if value is None:
                continue

            if value <= 0:
                continue

            if value not in normalized["loan_amounts"]:

                normalized["loan_amounts"].append(
                    value
                )

    # ---------------------------------------------------------
    # YEAR
    # ---------------------------------------------------------

    if normalized["car_year"] is not None:

        try:

            normalized["car_year"] = int(
                normalized["car_year"]
            )

        except (TypeError, ValueError):

            normalized["car_year"] = None

    # ---------------------------------------------------------
    # CAR VALUE
    # ---------------------------------------------------------

    if normalized["car_value"] is not None:

        normalized["car_value"] = normalize_number(
            normalized["car_value"]
        )

    # ---------------------------------------------------------
    # LOAN TERM
    # ---------------------------------------------------------

    if normalized["loan_term_months"] is not None:

        try:

            normalized["loan_term_months"] = int(
                normalized["loan_term_months"]
            )

        except (TypeError, ValueError):

            normalized["loan_term_months"] = None

    return normalized


# ============================================================
# INVALID AI VALUES
# ============================================================

def is_invalid_ai_value(
    field,
    value
):

    if value is None:
        return True

    if isinstance(value, str):

        value = value.strip().lower()

        if not value:
            return True

        # AI sometimes hallucinates generic words as car models.
        invalid_values = {

            "возможно",
            "возможно ли",
            "да",
            "нет",
            "не знаю",
            "автомобиль",
            "машина",
            "новый",
            "новая",
            "современный автомобиль",
            "современная машина",
        }

        if field == "car_model":

            if value in invalid_values:
                return True

            if value.startswith("возможно"):
                return True

    return False


# ============================================================
# MERGE AI + DETERMINISTIC EXTRACTION
# ============================================================

def merge_extractions(
    ai_information,
    deterministic_information,
):

    ai = normalize_information(
        ai_information
    )

    deterministic = normalize_information(
        deterministic_information
    )

    merged = empty_information()

    # ---------------------------------------------------------
    # SIMPLE FIELDS
    #
    # DETERMINISTIC HAS PRIORITY.
    #
    # This is intentional.
    #
    # Example:
    #
    # AI:
    #     car_model = "возможно"
    #
    # Deterministic:
    #     car_model = "BYD Song Plus"
    #
    # Final:
    #     car_model = "BYD Song Plus"
    # ---------------------------------------------------------

    for field in (
        "car_model",
        "car_year",
        "car_value",
        "loan_program",
        "vehicle_possession",
        "registration_region",
        "loan_term_months",
    ):

        deterministic_value = deterministic.get(
            field
        )

        ai_value = ai.get(
            field
        )

        # -----------------------------------------------------
        # Deterministic value wins when valid.
        # -----------------------------------------------------

        if not is_invalid_ai_value(
            field,
            deterministic_value
        ):

            merged[field] = deterministic_value

            continue

        # -----------------------------------------------------
        # Otherwise use AI value if valid.
        # -----------------------------------------------------

        if not is_invalid_ai_value(
            field,
            ai_value
        ):

            merged[field] = ai_value

    # ---------------------------------------------------------
    # LOAN AMOUNT
    #
    # Deterministic extraction has priority because it uses
    # explicit Russian loan-request patterns.
    # ---------------------------------------------------------

    deterministic_loan = normalize_number(
        deterministic.get(
            "loan_amount"
        )
    )

    ai_loan = normalize_number(
        ai.get(
            "loan_amount"
        )
    )

    if (
        deterministic_loan is not None
        and deterministic_loan > 0
    ):

        merged["loan_amount"] = (
            deterministic_loan
        )

        merged["loan_amounts"] = [
            deterministic_loan
        ]

    elif (
        ai_loan is not None
        and ai_loan > 0
    ):

        merged["loan_amount"] = (
            ai_loan
        )

        merged["loan_amounts"] = [
            ai_loan
        ]

    else:

        # -----------------------------------------------------
        # Preserve valid AI amount list.
        # -----------------------------------------------------

        for amount in ai.get(
            "loan_amounts",
            []
        ):

            value = normalize_number(
                amount
            )

            if value is None:
                continue

            if value <= 0:
                continue

            if value not in merged["loan_amounts"]:

                merged["loan_amounts"].append(
                    value
                )

    return merged


# ============================================================
# CHOOSE LOAN AMOUNT
# ============================================================

def choose_loan_amount(
    customer_message,
    loan_amounts,
    direct_loan_amount=None,
):

    # ---------------------------------------------------------
    # DIRECT VALUE
    # ---------------------------------------------------------

    direct = normalize_number(
        direct_loan_amount
    )

    if direct is not None and direct > 0:
        return direct

    # ---------------------------------------------------------
    # NO AMOUNTS
    # ---------------------------------------------------------

    if not loan_amounts:
        return None

    amounts = []

    for value in loan_amounts:

        normalized = normalize_number(
            value
        )

        if normalized is None:
            continue

        if normalized <= 0:
            continue

        if normalized not in amounts:

            amounts.append(
                normalized
            )

    if not amounts:
        return None

    # ---------------------------------------------------------
    # CUSTOMER MESSAGE
    # ---------------------------------------------------------

    text = (
        customer_message
        .lower()
        .replace(",", " ")
    )

    patterns = [

        r"(хотим|хочу|нужен|нужно|нужны)"
        r".{0,100}?(\d[\d\s]{2,})",

        r"(получить|выдать|займ|займа)"
        r".{0,100}?(\d[\d\s]{2,})",

        r"(запрашиваем|запрошенная сумма)"
        r".{0,100}?(\d[\d\s]{2,})",
    ]

    candidates = []

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        for match in matches:

            try:

                number_text = (
                    match[-1]
                    .replace(" ", "")
                )

                value = float(
                    number_text
                )

                candidates.append(
                    value
                )

            except (
                TypeError,
                ValueError
            ):

                continue

    # ---------------------------------------------------------
    # MATCH CUSTOMER REQUEST
    # ---------------------------------------------------------

    for candidate in candidates:

        for amount in amounts:

            if abs(candidate - amount) < 0.01:

                return amount

    # ---------------------------------------------------------
    # ONLY ONE AMOUNT
    # ---------------------------------------------------------

    if len(amounts) == 1:

        return amounts[0]

    # ---------------------------------------------------------
    # AMBIGUOUS
    # ---------------------------------------------------------

    return None
# ============================================================
# BARE REGISTRATION REGION FALLBACK
# ============================================================

def extract_bare_registration_region(
    customer_message: str
):
    if not isinstance(customer_message, str):
        return None

    value = customer_message.strip()

    if not value:
        return None

    regions = {
        "бишкек": "Бишкек",
        "бишкеке": "Бишкек",
        "ош": "Ош",
        "оше": "Ош",
        "нарыне": "Нарын",
        "таласе": "Талас",
        "баткене": "Баткен",
        "чуе": "Чуй",
        "иссык-куле": "Иссык-Куль",
        "джалал-абаде": "Джалал-Абад",
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


# ============================================================
# UPDATE CUSTOMER
# ============================================================

def update_customer_from_information(
    customer: CustomerCard,
    information: dict,
    customer_message: str
):

    information = normalize_information(
        information
    )

    # ---------------------------------------------------------
    # CAR MODEL
    # ---------------------------------------------------------

    if information["car_model"]:

        customer.car_model = (
            information["car_model"]
        )

    # ---------------------------------------------------------
    # CAR YEAR
    # ---------------------------------------------------------

    if information["car_year"] is not None:

        customer.car_year = (
            information["car_year"]
        )

    # ---------------------------------------------------------
    # CAR VALUE
    # ---------------------------------------------------------

    if information["car_value"] is not None:

        customer.car_value = (
            information["car_value"]
        )

    # ---------------------------------------------------------
    # LOAN AMOUNT
    # ---------------------------------------------------------

    loan_amount = choose_loan_amount(

        customer_message,

        information["loan_amounts"],

        information.get(
            "loan_amount"
        )
    )

    if loan_amount is not None:

        customer.loan_amount = (
            loan_amount
        )

    # ---------------------------------------------------------
    # LOAN PROGRAM
    # ---------------------------------------------------------

    if (
        information["loan_program"]
        and customer.loan_program is None
    ):

        customer.loan_program = (
            information["loan_program"]
        )

    # ---------------------------------------------------------
    # VEHICLE POSSESSION
    # ---------------------------------------------------------

    if information["vehicle_possession"]:

        customer.vehicle_possession = (
            information["vehicle_possession"]
        )

    # ---------------------------------------------------------
    # REGISTRATION REGION
    # ---------------------------------------------------------

    if information["registration_region"]:

        normalized_region = normalize_information({
            "registration_region":
                information["registration_region"]
        })["registration_region"]

        if normalized_region:

            customer.registration_region = (
                normalized_region
            )

    else:

        bare_region = extract_bare_registration_region(
            customer_message
        )

        if bare_region:

            normalized_region = normalize_information({
                "registration_region":
                    bare_region
            })["registration_region"]

            if normalized_region:

                customer.registration_region = (
                    normalized_region
                )

    # ---------------------------------------------------------
    # LOAN TERM
    # ---------------------------------------------------------

    if information["loan_term_months"] is not None:

        customer.loan_term_months = (
            information["loan_term_months"]
        )


    print("AFTER UPDATE DEBUG:")
    print("car_model:", customer.car_model)
    print("car_year:", customer.car_year)
    print("car_value:", customer.car_value)
    print("loan_amount:", customer.loan_amount)
    print("loan_program:", customer.loan_program)
    print("vehicle_possession:", customer.vehicle_possession)
    print("registration_region:", customer.registration_region)

# ============================================================
# NEXT REQUIRED FIELD
# ============================================================
def get_next_required_field(
    customer: CustomerCard
):

    # ---------------------------------------------------------
    # VEHICLE
    # ---------------------------------------------------------

    if not customer.car_model:
        return "car_model"

    if customer.car_year is None:
        return "car_year"

    if customer.car_value is None:
        return "car_value"

    # ---------------------------------------------------------
    # LOAN
    # ---------------------------------------------------------

    if customer.loan_amount is None:
        return "loan_amount"

    if not customer.loan_program:
        return "loan_program"

    # ---------------------------------------------------------
    # VEHICLE POSSESSION
    # ---------------------------------------------------------

    if customer.vehicle_possession is None:
        return "vehicle_possession"

    # ---------------------------------------------------------
    # CUSTOMER
    # ---------------------------------------------------------

    if not customer.registration_region:
        return "registration_region"

    # ---------------------------------------------------------
    # LOAN TERM
    # ---------------------------------------------------------

    if customer.loan_term_months is None:
        return "loan_term_months"

    return None


# ============================================================
# QUESTIONS
# ============================================================
def get_question_for_field(
    field
):

    questions = {

        "car_model":
            "Подскажите, пожалуйста, модель автомобиля.",

        "car_year":
            "Подскажите, пожалуйста, год выпуска автомобиля.",

        "car_value":
            "Подскажите, пожалуйста, примерную стоимость автомобиля.",

        "loan_amount":
            "Подскажите, пожалуйста, какую сумму займа вы хотите получить.",

        "loan_program":
            "Подскажите, пожалуйста, какую программу займа вы рассматриваете?",

        "vehicle_possession":
            (
                "Подскажите, пожалуйста, Вас интересует "
                "займ без изъятия автомобиля или с "
                "размещением автомобиля на охраняемой стоянке?"
            ),

        "registration_region":
            "В каком регионе вы зарегистрированы?",

        "loan_term_months":
            "Подскажите, пожалуйста, на какой срок вы хотите оформить займ?",
    }

    return questions.get(
        field,
        "Пожалуйста, предоставьте недостающую информацию."
    )



# ============================================================
# MONEY FORMAT
# ============================================================

def format_money(value):

    if value is None:
        return "0"

    try:

        return f"{float(value):,.0f}"

    except (
        TypeError,
        ValueError
    ):

        return str(value)


# ============================================================
# APPROVAL
# ============================================================

def build_approval_response(
    customer
):

    loan_amount = format_money(
        customer.loan_amount
    )

    car_value = format_money(
        customer.car_value
    )

    return (
        "Предварительная проверка вашей заявки "
        "пройдена успешно. "
        f"Запрошенная сумма составляет "
        f"{loan_amount} сом, "
        f"примерная стоимость автомобиля — "
        f"{car_value} сом. "
        "Ваша заявка предварительно одобрена."
    )


# ============================================================
# REJECTION
# ============================================================

def build_rejection_response(
    customer
):

    return (
        "К сожалению, по результатам "
        "предварительной проверки мы "
        "не можем одобрить вашу заявку."
    )


# ============================================================
# INFORMATION ACKNOWLEDGEMENT
# ============================================================

def build_information_acknowledgement(
    information: dict
):
    parts = []

    if information.get("car_model"):
        parts.append(
            f"Модель автомобиля — {information['car_model']}"
        )

    if information.get("car_year") is not None:
        parts.append(
            f"год выпуска — {information['car_year']}"
        )

    if information.get("car_value") is not None:
        parts.append(
            f"стоимость автомобиля — {information['car_value']}"
        )

    if information.get("loan_amount") is not None:
        parts.append(
            f"сумма займа — {information['loan_amount']}"
        )

    if information.get("loan_program"):
        parts.append(
            f"программа — {information['loan_program']}"
        )

    if information.get("vehicle_possession"):
        if information["vehicle_possession"] == "customer":
            parts.append(
                "автомобиль останется у вас"
            )
        elif information["vehicle_possession"] == "lender":
            parts.append(
                "автомобиль будет размещён на охраняемой стоянке"
            )

    if information.get("registration_region"):
        parts.append(
            f"регион регистрации — {information['registration_region']}"
        )

    if not parts:
        return None

    return "Принял, " + ", ".join(parts) + "."



# ============================================================
# CONTEXT-AWARE BARE MONEY EXTRACTION
# ============================================================

def extract_bare_money_answer(
    message
):
    """
    Extract a natural money answer when the customer is answering
    a money-related question.

    Supports examples such as:
        1500000
        1 500 000
        20 тыс
        20 тыс долларов
        20 тысяч долларов
        500 тыс сом
        1.5 млн сом
        1,5 млн долларов
    """

    if not message:
        return None

    text = str(message).strip().lower()
    text = text.replace("\xa0", " ")

    # ---------------------------------------------------------
    # NATURAL APPROXIMATION PREFIXES
    #
    # Customers commonly answer:
    #   "примерно 1500000 сом"
    #   "около 1500000 сом"
    #   "примерно 1.5 млн сом"
    #
    # These prefixes do not change the numeric meaning.
    # ---------------------------------------------------------

    text = re.sub(
        r"^(?:примерно|около|приблизительно|ориентировочно)\s+",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # Normalize common currency spellings.
    text = re.sub(
        r"\b(?:сом|сомов|сома|com|долларов|доллара|доллар|\$|usd)\b",
        "",
        text,
        flags=re.IGNORECASE,
    ).strip()

    # ---------------------------------------------------------
    # THOUSANDS
    # ---------------------------------------------------------

    match = re.fullmatch(
        r"(\d+(?:[.,]\d+)?)\s*(?:тыс\.?|тысяч|к)",
        text,
        flags=re.IGNORECASE,
    )

    if match:
        value = normalize_number(match.group(1))

        if value is not None and value > 0:
            return value * 1000

    # ---------------------------------------------------------
    # MILLIONS
    # ---------------------------------------------------------

    match = re.fullmatch(
        r"(\d+(?:[.,]\d+)?)\s*(?:млн\.?|миллион(?:а|ов)?)",
        text,
        flags=re.IGNORECASE,
    )

    if match:
        value = normalize_number(match.group(1))

        if value is not None and value > 0:
            return value * 1_000_000

    # ---------------------------------------------------------
    # PLAIN NUMBER
    # ---------------------------------------------------------

    if not re.fullmatch(
        r"\d{1,3}(?:[\s,.]\d{3})+|\d+(?:[.,]\d+)?",
        text,
    ):
        return None

    value = normalize_number(text)

    if value is None or value <= 0:
        return None

    return value


# ============================================================
# PROCESS MESSAGE
# ============================================================

def process_conversation_message(
    customer: CustomerCard,
    message: str
):

    errors = []

    # ========================================================
    # ALREADY DECIDED
    # ========================================================

    if customer.stage in (
        "approved",
        "rejected",
        "completed"
    ):

        if customer.decision == "approved":

            response = (
                "Ваша заявка уже была "
                "предварительно одобрена."
            )

        elif customer.decision == "rejected":

            response = (
                "По вашей заявке уже принято "
                "решение об отказе."
            )

        else:

            response = (
                "По вашей заявке уже принято решение."
            )

        return {

            "application_id":
                customer.application_id,

            "customer":
                customer,

            "status":
                "decision_already_made",

            "response":
                response,

            "stage":
                customer.stage,

            "decision":
                customer.decision,

            "decision_reason":
                customer.decision_reason,

            "next_field":
                None,

            "errors":
                errors
        }

    # ========================================================
    # EXTRACTION
    # ========================================================

    try:

        # ----------------------------------------------------
        # AI EXTRACTION
        # ----------------------------------------------------

        try:

            ai_information = (
                extract_information_with_ai(
                    message
                )
            )

        except Exception as error:

            print(
                "[AI EXTRACTION WARNING]",
                error
            )

            ai_information = (
                empty_information()
            )

        # ----------------------------------------------------
        # DETERMINISTIC EXTRACTION
        # ----------------------------------------------------

        deterministic_information = (
            extract_deterministic_fields(
                message
            )
        )

        # ----------------------------------------------------
        # MERGE
        # ----------------------------------------------------

        information = merge_extractions(

            ai_information,

            deterministic_information
        )

        information = normalize_information(
            information
        )

        # ----------------------------------------------------
        # DEBUG
        # ----------------------------------------------------

        print()
        print(
            "[EXTRACTION DEBUG]"
        )

        print(
            "Customer message:"
        )

        print(
            message
        )

        print()

        print(
            "AI extraction:"
        )

        print(
            ai_information
        )

        print()

        print(
            "Deterministic extraction:"
        )

        print(
            deterministic_information
        )

        print()

        print(
            "Final merged extraction:"
        )

        print(
            information
        )

        print(
            "[END EXTRACTION DEBUG]"
        )

        print()

    except Exception as error:

        errors.append(
            str(error)
        )

        information = (
            empty_information()
        )

    # ========================================================
    # CONTEXT-AWARE MONEY ANSWER
    #
    # The same number can mean different things depending on
    # the question Aylin is currently asking.
    #
    # Example:
    #
    # Aylin:
    #   "Подскажите, пожалуйста, примерную стоимость автомобиля."
    #
    # Customer:
    #   "20 тыс долларов"
    #
    # This MUST become car_value, not loan_amount.
    #
    # Likewise:
    #
    # Aylin:
    #   "Подскажите, пожалуйста, какую сумму займа вы хотите получить."
    #
    # Customer:
    #   "500 тыс сом"
    #
    # This MUST become loan_amount.
    # ========================================================

    current_field = get_next_required_field(
        customer
    )

    if current_field in {
        "car_value",
        "loan_amount",
    }:

        bare_value = extract_bare_money_answer(
            message
        )

        if bare_value is not None:

            # ------------------------------------------------
            # CAR VALUE CONTEXT
            # ------------------------------------------------

            if current_field == "car_value":

                information["car_value"] = (
                    bare_value
                )

                # A generic deterministic extractor may have
                # interpreted the same number as a loan amount.
                # Remove that interpretation because the current
                # question is explicitly about vehicle value.

                information["loan_amount"] = None

                information["loan_amounts"] = []

                print(
                    "[CONTEXT EXTRACTION] "
                    "car_value:",
                    bare_value
                )

            # ------------------------------------------------
            # LOAN AMOUNT CONTEXT
            # ------------------------------------------------

            elif current_field == "loan_amount":

                information["loan_amount"] = (
                    bare_value
                )

                information["loan_amounts"] = [
                    bare_value
                ]

                print(
                    "[CONTEXT EXTRACTION] "
                    "loan_amount:",
                    bare_value
                )

    # ========================================================
    # UPDATE CUSTOMER
    # ========================================================

    update_customer_from_information(

        customer,

        information,

        message
    )

    # ========================================================
    # NEXT REQUIRED FIELD
    # ========================================================

    next_field = (
        get_next_required_field(
            customer
        )
    )

    # ========================================================
    # ASK CUSTOMER
    # ========================================================

    if next_field:

        customer.stage = (
            "collecting_information"
        )

        return {

            "application_id":
                customer.application_id,

            "customer":
                customer,

            "status":
                "waiting_for_customer",

            "response":
                get_question_for_field(
                    next_field
                ),

            "stage":
                customer.stage,

            "decision":
                None,

            "decision_reason":
                None,

            "next_field":
                next_field,

            "errors":
                errors
        }

    # ========================================================
    # DECISION
    # ========================================================

    customer.stage = (
        "checking_application"
    )

    try:

        decision = evaluate_application(
            customer
        )

    except Exception as error:

        errors.append(
            str(error)
        )

        customer.stage = (
            "collecting_information"
        )

        return {

            "application_id":
                customer.application_id,

            "customer":
                customer,

            "status":
                "error",

            "response":
                (
                    "Не удалось выполнить "
                    "предварительную проверку заявки. "
                    "Пожалуйста, попробуйте ещё раз."
                ),

            "stage":
                customer.stage,

            "decision":
                None,

            "decision_reason":
                None,

            "next_field":
                None,

            "errors":
                errors
        }

    # ========================================================
    # SAVE DECISION
    # ========================================================

    if isinstance(decision, dict):

        decision_name = decision.get(
            "decision"
        )

        decision_reason = decision.get(
            "reason"
        )

        if decision_name:

            customer.decision = (
                decision_name
            )

        if decision_reason:

            customer.decision_reason = (
                decision_reason
            )

    # ========================================================
    # APPROVED
    # ========================================================

    if customer.decision == "approved":

        customer.stage = (
            "approved"
        )

        return {

            "application_id":
                customer.application_id,

            "customer":
                customer,

            "status":
                "decision_ready",

            "response":
                build_approval_response(
                    customer
                ),

            "stage":
                customer.stage,

            "decision":
                decision,

            "decision_reason":
                customer.decision_reason,

            "next_field":
                None,

            "errors":
                errors
        }

    # ========================================================
    # REJECTED
    # ========================================================

    if customer.decision == "rejected":

        customer.stage = (
            "rejected"
        )

        return {

            "application_id":
                customer.application_id,

            "customer":
                customer,

            "status":
                "decision_ready",

            "response":
                build_rejection_response(
                    customer
                ),

            "stage":
                customer.stage,

            "decision":
                decision,

            "decision_reason":
                customer.decision_reason,

            "next_field":
                None,

            "errors":
                errors
        }

    # ========================================================
    # PENDING
    # ========================================================

    customer.stage = (
        "decision_pending"
    )

    return {

        "application_id":
            customer.application_id,

        "customer":
            customer,

        "status":
            "decision_pending",

        "response":
            (
                "Ваша заявка передана "
                "на дополнительную проверку."
            ),

        "stage":
            customer.stage,

        "decision":
            decision,

        "decision_reason":
            customer.decision_reason,

        "next_field":
            None,

        "errors":
            errors
    }

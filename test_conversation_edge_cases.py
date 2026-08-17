# ============================================================
# AYLIN CONVERSATION EDGE CASE TESTS
# Compatible with the existing function-based architecture
# ============================================================

from conversation_manager import (
    CustomerCard,
    process_conversation_message,
)


# ============================================================
# HELPERS
# ============================================================

def print_separator(title=None):

    print("\n" + "=" * 70)

    if title:
        print(title)
        print("=" * 70)


def show_result(result):

    print("\nAYLIN:")

    if isinstance(result, dict):

        print(
            result.get(
                "response",
                result.get("message", "")
            )
        )

        print("\nSTATUS:")
        print(result.get("status"))

        print("\nNEXT FIELD:")
        print(result.get("next_field"))

        print("\nSTAGE:")
        print(result.get("stage"))

        print("\nDECISION:")
        print(result.get("decision"))

        print("\nDECISION REASON:")
        print(result.get("decision_reason"))

        print("\nERRORS:")
        print(result.get("errors"))

    else:

        print(result)


def show_card(card):

    print("\nCURRENT CUSTOMER CARD")
    print("-" * 70)

    fields = [
        "application_id",
        "phone",
        "car_model",
        "car_year",
        "car_value",
        "loan_amount",
        "loan_program",
        "registration_region",
        "stage",
        "decision",
        "decision_reason",
    ]

    for field in fields:

        value = getattr(
            card,
            field,
            None
        )

        print(
            f"{field}: {value}"
        )


# ============================================================
# PROCESS MESSAGE COMPATIBILITY
# ============================================================

def process_message(
    card,
    message
):
    """
    Wrapper around the existing
    process_conversation_message()
    function.

    We try the common argument layouts so the
    test remains compatible with the current
    implementation.
    """

    attempts = [

        lambda:
        process_conversation_message(
            card,
            message
        ),

        lambda:
        process_conversation_message(
            message,
            card
        ),

    ]

    last_error = None

    for attempt in attempts:

        try:

            return attempt()

        except TypeError as error:

            last_error = error

    raise last_error


# ============================================================
# CREATE CUSTOMER CARD
# ============================================================

def create_card(
    phone,
    application_id
):

    """
    Create a CustomerCard using the existing
    project model.

    The function tries the most common constructor
    formats used by this project.
    """

    attempts = [

        lambda:
        CustomerCard(
            application_id=application_id,
            phone=phone
        ),

        lambda:
        CustomerCard(
            phone=phone,
            application_id=application_id
        ),

        lambda:
        CustomerCard(
            application_id,
            phone
        ),

    ]

    last_error = None

    for attempt in attempts:

        try:

            return attempt()

        except TypeError as error:

            last_error = error

    raise last_error


# ============================================================
# RUN SINGLE TURN
# ============================================================

def run_turn(
    card,
    message,
    turn_number
):

    print_separator(
        f"TURN {turn_number}"
    )

    print("\nCUSTOMER:")
    print(message)

    try:

        result = process_message(
            card,
            message
        )

    except Exception as error:

        print("\nERROR:")
        print(
            type(error).__name__,
            str(error)
        )

        return None

    show_result(result)

    print()

    show_card(card)

    return result


# ============================================================
# TEST 1
# ALL INFORMATION IN ONE MESSAGE
# ============================================================

def test_all_information_one_message():

    print_separator(
        "TEST 1 — ALL INFORMATION IN ONE MESSAGE"
    )

    card = create_card(
        "+996EDGE001",
        "APP-EDGE-001"
    )

    message = """
    Здравствуйте.

    Это BYD Song Plus, 2024 года.
    Примерная стоимость автомобиля 1 500 000 сом.
    Хотим получить 400 000 сом под автозалог,
    но без передачи автомобиля.

    Я зарегистрирована в Бишкеке.
    """

    run_turn(
        card,
        message,
        1
    )


# ============================================================
# TEST 2
# INFORMATION IN DIFFERENT ORDER
# ============================================================

def test_information_different_order():

    print_separator(
        "TEST 2 — INFORMATION IN DIFFERENT ORDER"
    )

    card = create_card(
        "+996EDGE002",
        "APP-EDGE-002"
    )

    messages = [

        """
        Я зарегистрирована в Бишкеке.
        Мне нужен автозалог без передачи автомобиля.
        """,

        """
        Сумма нужна 500 000 сом.
        """,

        """
        Машина стоит примерно 1 800 000 сом.
        """,

        """
        Это BYD Song Plus.
        """,

        """
        Автомобиль 2024 года.
        """,
    ]

    for index, message in enumerate(
        messages,
        start=1
    ):

        run_turn(
            card,
            message,
            index
        )


# ============================================================
# TEST 3
# CUSTOMER CHANGES LOAN AMOUNT
# ============================================================

def test_loan_amount_change():

    print_separator(
        "TEST 3 — CUSTOMER CHANGES LOAN AMOUNT"
    )

    card = create_card(
        "+996EDGE003",
        "APP-EDGE-003"
    )

    messages = [

        """
        Это BYD Song Plus, 2024 года.
        Стоимость автомобиля примерно 1 500 000 сом.
        Я зарегистрирована в Бишкеке.
        Автозалог без передачи автомобиля.
        Хочу получить 600 000 сом.
        """,

        """
        Я передумала.
        Давайте лучше 400 000 сом.
        """,
    ]

    for index, message in enumerate(
        messages,
        start=1
    ):

        run_turn(
            card,
            message,
            index
        )

    print_separator(
        "TEST 3 FINAL CHECK"
    )

    print(
        "EXPECTED LOAN AMOUNT: 400000.0"
    )

    print(
        "ACTUAL LOAN AMOUNT:",
        getattr(
            card,
            "loan_amount",
            None
        )
    )


# ============================================================
# TEST 4
# LOAN AMOUNT FIRST
# ============================================================

def test_loan_amount_first():

    print_separator(
        "TEST 4 — LOAN AMOUNT FIRST"
    )

    card = create_card(
        "+996EDGE004",
        "APP-EDGE-004"
    )

    messages = [

        "Мне нужно 400 000 сом.",

        "Автомобиль BYD Song Plus.",

        "2024 года.",

        "Стоимость примерно 1 500 000 сом.",

        "Автозалог без передачи автомобиля.",

        "Я зарегистрирована в Бишкеке.",
    ]

    for index, message in enumerate(
        messages,
        start=1
    ):

        run_turn(
            card,
            message,
            index
        )


# ============================================================
# TEST 5
# CAR INFORMATION FIRST
# ============================================================

def test_car_information_first():

    print_separator(
        "TEST 5 — CAR INFORMATION FIRST"
    )

    card = create_card(
        "+996EDGE005",
        "APP-EDGE-005"
    )

    messages = [

        "Это BYD Song Plus.",

        "2024 года.",

        "Стоимость автомобиля 1 500 000 сом.",

        "Хочу 400 000 сом.",

        "Автозалог без передачи автомобиля.",

        "Я зарегистрирована в Бишкеке.",
    ]

    for index, message in enumerate(
        messages,
        start=1
    ):

        run_turn(
            card,
            message,
            index
        )


# ============================================================
# TEST 6
# DIFFERENT NUMBER FORMATS
# ============================================================

def test_number_formats():

    print_separator(
        "TEST 6 — DIFFERENT NUMBER FORMATS"
    )

    card = create_card(
        "+996EDGE006",
        "APP-EDGE-006"
    )

    messages = [

        """
        Это BYD Song Plus, 2024 года.
        """,

        """
        Стоимость автомобиля примерно 1.500.000 сом.
        """,

        """
        Хочу получить 400000 сом.
        """,

        """
        Автозалог без передачи автомобиля.
        """,

        """
        Я зарегистрирована в Бишкеке.
        """,
    ]

    for index, message in enumerate(
        messages,
        start=1
    ):

        run_turn(
            card,
            message,
            index
        )


# ============================================================
# TEST 7
# ALTERNATIVE LOAN AMOUNTS
# ============================================================

def test_alternative_loan_amounts():

    print_separator(
        "TEST 7 — ALTERNATIVE LOAN AMOUNTS"
    )

    card = create_card(
        "+996EDGE007",
        "APP-EDGE-007"
    )

    message = """
    Это BYD Song Plus, 2024 года.
    Стоимость автомобиля 1 500 000 сом.

    Сначала хотели получить 400 000 сом.
    Можно рассмотреть 100 000–150 000 сом.
    В идеале хотелось бы до 600 000 сом.

    Автозалог без передачи автомобиля.
    Я зарегистрирована в Бишкеке.
    """

    run_turn(
        card,
        message,
        1
    )

    print_separator(
        "TEST 7 EXPECTATION"
    )

    print(
        "PRIMARY REQUEST SHOULD PREFERABLY BE 400000.0"
    )

    print(
        "ACTUAL:",
        getattr(
            card,
            "loan_amount",
            None
        )
    )


# ============================================================
# TEST 8
# CUSTOMER ASKS QUESTION
# ============================================================

def test_customer_question():

    print_separator(
        "TEST 8 — CUSTOMER ASKS A QUESTION"
    )

    card = create_card(
        "+996EDGE008",
        "APP-EDGE-008"
    )

    messages = [

        """
        Здравствуйте, хочу получить деньги под автомобиль.
        """,

        """
        А можно оставить автомобиль у себя
        и продолжать им пользоваться?
        """,

        """
        Это BYD Song Plus.
        """,

        """
        2024 года.
        """,

        """
        Стоимость около 1 500 000 сом.
        """,

        """
        Хотим 400 000 сом.
        """,

        """
        Автозалог без передачи автомобиля.
        """,

        """
        Я зарегистрирована в Бишкеке.
        """,
    ]

    for index, message in enumerate(
        messages,
        start=1
    ):

        run_turn(
            card,
            message,
            index
        )


# ============================================================
# TEST 9
# MISSING REGION
# ============================================================

def test_missing_region():

    print_separator(
        "TEST 9 — MISSING REGISTRATION REGION"
    )

    card = create_card(
        "+996EDGE009",
        "APP-EDGE-009"
    )

    message = """
    Это BYD Song Plus, 2024 года.
    Стоимость автомобиля 1 500 000 сом.
    Хочу получить 400 000 сом.
    Автозалог без передачи автомобиля.
    """

    run_turn(
        card,
        message,
        1
    )

    print_separator(
        "TEST 9 EXPECTATION"
    )

    print(
        "Aylin should ask for registration region."
    )


# ============================================================
# TEST 10
# CONFLICTING CAR VALUE
# ============================================================

def test_conflicting_car_value():

    print_separator(
        "TEST 10 — CONFLICTING CAR VALUE"
    )

    card = create_card(
        "+996EDGE010",
        "APP-EDGE-010"
    )

    messages = [

        """
        Это BYD Song Plus, 2024 года.
        Стоимость автомобиля примерно 1 500 000 сом.
        Хочу 400 000 сом.
        Автозалог без передачи автомобиля.
        Я зарегистрирована в Бишкеке.
        """,

        """
        Я уточнила стоимость.
        На самом деле автомобиль стоит около 1 600 000 сом.
        """,
    ]

    for index, message in enumerate(
        messages,
        start=1
    ):

        run_turn(
            card,
            message,
            index
        )

    print_separator(
        "TEST 10 FINAL CHECK"
    )

    print(
        "CURRENT CAR VALUE:",
        getattr(
            card,
            "car_value",
            None
        )
    )


# ============================================================
# TEST 11
# REALISTIC SHORT CONVERSATION
# ============================================================

def test_realistic_short_conversation():

    print_separator(
        "TEST 11 — REALISTIC SHORT CONVERSATION"
    )

    card = create_card(
        "+996EDGE011",
        "APP-EDGE-011"
    )

    messages = [

        """
        Здравствуйте, хочу получить деньги под автомобиль.
        """,

        """
        Это BYD Song Plus.
        """,

        """
        2024 года, автомобиль практически новый.
        """,

        """
        Думаю, его стоимость около 1 500 000 сом.
        """,

        """
        Мне нужно 400 000 сом.
        """,

        """
        Хотела бы оформить автозалог
        без передачи автомобиля.
        """,

        """
        Я зарегистрирована в Бишкеке.
        """,
    ]

    for index, message in enumerate(
        messages,
        start=1
    ):

        run_turn(
            card,
            message,
            index
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n")

    print("=" * 70)
    print("AYLIN CONVERSATION EDGE CASE TEST SUITE")
    print("=" * 70)

    print(
        "\nTesting the existing function-based "
        "conversation_manager.py architecture."
    )

    print("\nTests:")

    print("1.  All information in one message")
    print("2.  Information in different order")
    print("3.  Customer changes loan amount")
    print("4.  Loan amount first")
    print("5.  Car information first")
    print("6.  Different number formats")
    print("7.  Alternative loan amounts")
    print("8.  Customer asks a question")
    print("9.  Missing registration region")
    print("10. Conflicting car value")
    print("11. Realistic short conversation")

    # --------------------------------------------------------
    # Run
    # --------------------------------------------------------

    test_all_information_one_message()

    test_information_different_order()

    test_loan_amount_change()

    test_loan_amount_first()

    test_car_information_first()

    test_number_formats()

    test_alternative_loan_amounts()

    test_customer_question()

    test_missing_region()

    test_conflicting_car_value()

    test_realistic_short_conversation()

    # --------------------------------------------------------
    # Complete
    # --------------------------------------------------------

    print_separator(
        "EDGE CASE TEST SUITE COMPLETE"
    )

    print(
        "\nReview the results above."
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
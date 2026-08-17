from uuid import uuid4

from conversation_application import (
    process_conversation_message
)

from customer_card import CustomerCard

from application_repository import (
    create_application_table,
    save_customer
)


# ============================================================
# TEST CONFIGURATION
# ============================================================

TEST_PHONE = (
    "+996TEST"
    + uuid4().hex[:8]
)

APPLICATION_ID = (
    "APP-TEST-"
    + uuid4().hex[:8].upper()
)


# ============================================================
# CLIENT CONVERSATION
# ============================================================

MESSAGES = [

    # --------------------------------------------------------
    # MESSAGE 1
    # Original client audio transcription
    # --------------------------------------------------------

    """
Здравствуйте. Я вчера вам звонила по поводу автомобиля, да,
хотели бы использовать его в качестве залога.

Я отправлю вам фотографию этого нового современного автомобиля.
Мы хотели бы получить под него 400 000 сом. Это возможно?

Пожалуйста, рассчитайте сумму 400 000 сом без передачи автомобиля.
Мы сами являемся владельцами автомобиля, муж находится здесь со мной.
Мы можем сразу подписать все необходимые документы, чтобы всё было
оформлено правильно.

Нам нужно 400 000 сом на один месяц.

Если по какой-либо причине мы не сможем погасить займ в течение этого
месяца, какие будут условия на второй месяц? Можно ли просто оплатить
проценты и продлить займ ещё на один месяц?

Наталья, пожалуйста, объясните, как работает ставка 2,3%.
Это ежемесячная процентная ставка? Проценты оплачиваются каждый месяц
заранее? Как вообще работает ваша система? Это залог в ломбарде или
у вас другая система?

Рыночная стоимость похожего автомобиля, примерно с такими же
вложениями и в таком же состоянии, составляет около 350 000–370 000 сом.

Поэтому мы могли бы рассмотреть получение примерно 100 000–150 000 сом
под этот автомобиль.

В целом мы не хотим оставлять автомобиль у вас.
Вы можете выдать нам деньги, а мы продолжим сами пользоваться автомобилем.

Если это электромобиль, вы могли бы выдать под него до 600 000 сом,
при этом автомобиль останется у нас, и мы продолжим им пользоваться.
Мы не будем передавать автомобиль вам.

Пожалуйста, честно проверьте, какую процентную ставку вы можете нам
предложить.

Чем больше денег мы сможем получить, тем лучше, потому что деньги
нам срочно нужны.

В идеале мы хотели бы получить до 600 000 сом под этот конкретный
автомобиль.

Пожалуйста, точно рассчитайте для нас:
какой минимальный срок займа,
какая процентная ставка,
и какая будет общая сумма возврата.

Также расскажите, какой у вас юридический процесс.
Вы сами подготавливаете юридические документы и договор или нам нужно
самим подавать заявку?

Пожалуйста, объясните точно, какие документы и процедуры необходимы,
чтобы в дальнейшем у нас не возникло проблем.
""",

    # --------------------------------------------------------
    # MESSAGE 2
    # Customer provides car model
    # --------------------------------------------------------

    "Это BYD Song Plus.",

    # --------------------------------------------------------
    # MESSAGE 3
    # Customer provides car year
    # --------------------------------------------------------

    "2024 года.",

    # --------------------------------------------------------
    # MESSAGE 4
    # Customer provides vehicle value
    # --------------------------------------------------------

    "Примерная стоимость автомобиля 1 500 000 сом.",

    # --------------------------------------------------------
    # MESSAGE 5
    # Customer provides loan program
    # --------------------------------------------------------

    "Автозалог, но без передачи автомобиля.",

    # --------------------------------------------------------
    # MESSAGE 6
    # Customer provides registration region
    # --------------------------------------------------------

    "Я зарегистрирована в Бишкеке."
]


# ============================================================
# DISPLAY CUSTOMER CARD
# ============================================================

def print_customer_card(customer):

    print("\n")
    print("=" * 60)
    print("CURRENT CUSTOMER CARD")
    print("=" * 60)

    print(
        "Application ID:",
        customer.application_id
    )

    print(
        "Phone:",
        customer.phone
    )

    print(
        "Car model:",
        customer.car_model
    )

    print(
        "Car year:",
        customer.car_year
    )

    print(
        "Car value:",
        customer.car_value
    )

    print(
        "Loan amount:",
        customer.loan_amount
    )

    print(
        "Loan program:",
        customer.loan_program
    )

    print(
        "Registration region:",
        customer.registration_region
    )

    print(
        "Stage:",
        customer.stage
    )

    print(
        "Decision:",
        customer.decision
    )

    print(
        "Decision reason:",
        customer.decision_reason
    )


# ============================================================
# MAIN TEST
# ============================================================

def main():

    print("=" * 60)
    print("AYLIN MULTI-TURN REAL CLIENT TEST")
    print("=" * 60)

    print("\nTest phone:")
    print(TEST_PHONE)

    print("\nApplication ID:")
    print(APPLICATION_ID)

    # --------------------------------------------------------
    # Create database table
    # --------------------------------------------------------

    create_application_table()

    # --------------------------------------------------------
    # Create fresh customer/application
    # --------------------------------------------------------

    customer = CustomerCard(
        application_id=APPLICATION_ID,
        phone=TEST_PHONE,
        stage="new"
    )

    save_customer(customer)

    # ========================================================
    # PROCESS EACH CUSTOMER MESSAGE
    # ========================================================

    for index, message in enumerate(
        MESSAGES,
        start=1
    ):

        print("\n")
        print("=" * 60)
        print(
            f"TURN {index} / {len(MESSAGES)}"
        )
        print("=" * 60)

        print("\nCUSTOMER:")
        print(message.strip())

        try:

            result = process_conversation_message(
                customer,
                message
            )

            # ------------------------------------------------
            # Save current state
            # ------------------------------------------------

            save_customer(customer)

            print("\nAYLIN:")
            print(
                result.get(
                    "response",
                    "No response"
                )
            )

            # ------------------------------------------------
            # Result
            # ------------------------------------------------

            print("\nSTATUS:")
            print(
                result.get(
                    "status"
                )
            )

            print("\nNEXT FIELD:")
            print(
                result.get(
                    "next_field"
                )
            )

            print("\nSTAGE:")
            print(
                result.get(
                    "stage"
                )
            )

            print("\nDECISION:")
            print(
                result.get(
                    "decision"
                )
            )

            print("\nDECISION REASON:")
            print(
                result.get(
                    "decision_reason"
                )
            )

            print("\nERRORS:")
            print(
                result.get(
                    "errors",
                    []
                )
            )

            # ------------------------------------------------
            # Show card after every turn
            # ------------------------------------------------

            print_customer_card(
                customer
            )

        except Exception as error:

            print("\n")
            print("=" * 60)
            print("ERROR")
            print("=" * 60)

            print(
                type(error).__name__,
                ":",
                error
            )

            raise

    # ========================================================
    # FINAL RESULT
    # ========================================================

    print("\n")
    print("=" * 60)
    print("FINAL APPLICATION RESULT")
    print("=" * 60)

    print_customer_card(
        customer
    )

    print("\n")
    print("=" * 60)
    print("MULTI-TURN TEST COMPLETE")
    print("=" * 60)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()

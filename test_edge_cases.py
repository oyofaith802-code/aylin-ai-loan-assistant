from customer_card import CustomerCard
from conversation_manager import process_conversation_message


def print_result(turn, customer_message, result):
    print()
    print("=" * 70)
    print(f"TURN {turn}")
    print("=" * 70)

    print()
    print("CUSTOMER:")
    print(customer_message)

    print()
    print("AYLIN:")
    print(result["response"])

    print()
    print("STATUS:")
    print(result["status"])

    print()
    print("NEXT FIELD:")
    print(result["next_field"])

    print()
    print("STAGE:")
    print(result["stage"])

    print()
    print("DECISION:")
    print(result["decision"])

    print()
    print("DECISION REASON:")
    print(result["decision_reason"])

    print()
    print("ERRORS:")
    print(result["errors"])

    print()
    print("CURRENT CUSTOMER CARD")
    print("-" * 70)

    print("application_id:", customer.application_id)
    print("phone:", customer.phone)
    print("car_model:", customer.car_model)
    print("car_year:", customer.car_year)
    print("car_value:", customer.car_value)
    print("loan_amount:", customer.loan_amount)
    print("loan_program:", customer.loan_program)
    print("registration_region:", customer.registration_region)
    print("stage:", customer.stage)
    print("decision:", customer.decision)
    print("decision_reason:", customer.decision_reason)


# ============================================================
# TEST 1
# REALISTIC CONVERSATION
# ============================================================

print("=" * 70)
print("AYLIN EDGE CASE TEST SUITE")
print("=" * 70)


customer = CustomerCard(
    application_id="APP-EDGE-TEST",
    phone="+996EDGE000"
)


conversation = [

    "Здравствуйте, хочу получить деньги под автомобиль.",

    "Это BYD Song Plus.",

    "2024 года, автомобиль практически новый.",

    "Думаю, его стоимость около 1 500 000 сом.",

    "Мне нужно 400 000 сом.",

    "Хотела бы оформить автозалог без передачи автомобиля.",

    "Я зарегистрирована в Бишкеке."
]


for turn, message in enumerate(
    conversation,
    start=1
):

    result = process_conversation_message(
        customer,
        message
    )

    print_result(
        turn,
        message,
        result
    )


# ============================================================
# FINAL CHECK
# ============================================================

print()
print("=" * 70)
print("FINAL CHECK")
print("=" * 70)

print()

print("car_model:",
      customer.car_model)

print("car_year:",
      customer.car_year)

print("car_value:",
      customer.car_value)

print("loan_amount:",
      customer.loan_amount)

print("loan_program:",
      customer.loan_program)

print("registration_region:",
      customer.registration_region)

print("stage:",
      customer.stage)

print("decision:",
      customer.decision)

print("decision_reason:",
      customer.decision_reason)


# ============================================================
# EXPECTED VALUES
# ============================================================

print()
print("=" * 70)
print("EXPECTED")
print("=" * 70)

print("car_model: BYD Song Plus")
print("car_year: 2024")
print("car_value: 1500000.0")
print("loan_amount: 400000.0")
print("loan_program: Автозалог")
print("registration_region: Бишкеке")
print("stage: approved")
print("decision: approved")


# ============================================================
# VALIDATION
# ============================================================

print()
print("=" * 70)
print("VALIDATION")
print("=" * 70)

checks = {

    "car_model":
        customer.car_model == "BYD Song Plus",

    "car_year":
        customer.car_year == 2024,

    "car_value":
        customer.car_value == 1500000.0,

    "loan_amount":
        customer.loan_amount == 400000.0,

    "loan_program":
        customer.loan_program == "Автозалог",

    "registration_region":
        customer.registration_region == "Бишкеке",

    "stage":
        customer.stage == "approved",

    "decision":
        customer.decision == "approved"
}


all_passed = True


for field, passed in checks.items():

    if passed:

        print(
            f"PASS  {field}"
        )

    else:

        print(
            f"FAIL  {field}"
        )

        all_passed = False


print()
print("=" * 70)

if all_passed:

    print("ALL EDGE CASE TESTS PASSED")

else:

    print("SOME EDGE CASE TESTS FAILED")

print("=" * 70)
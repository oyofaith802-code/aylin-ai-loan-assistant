from customer_card import CustomerCard
from conversation_application import process_conversation_message


def print_result(title, result):
    print("=" * 60)
    print(title)
    print("=" * 60)
    print("Response:", result["response"])
    print("Status:", result["status"])
    print("Stage:", result["stage"])
    print("Decision:", result["decision"])
    print("Next field:", result["next_field"])
    print("Errors:", result["errors"])
    print()


# ============================================================
# TEST 1 — APPROVED APPLICATION
# ============================================================

customer = CustomerCard(
    application_id="APP-LIFECYCLE-001",
    phone="+996TEST-LIFE-001",
)

messages = [
    "Это BYD Song Plus.",
    "2024 года.",
    "Примерная стоимость автомобиля 1 500 000 сом.",
    "400 000 сом.",
    "Автозалог, без передачи автомобиля.",
    "Я зарегистрирована в Бишкеке.",
]

for index, message in enumerate(messages, 1):

    result = process_conversation_message(
        customer,
        message
    )

    print_result(
        f"APPROVAL TEST — TURN {index}",
        result
    )


print("=" * 60)
print("FINAL DECISION")
print("=" * 60)
print("Stage:", customer.stage)
print("Decision:", customer.decision)
print("Loan amount:", customer.loan_amount)
print()


# ============================================================
# TEST 2 — MESSAGE AFTER APPROVAL
# ============================================================

result = process_conversation_message(
    customer,
    "Я хочу изменить сумму займа на 600 000 сом."
)

print_result(
    "MESSAGE AFTER APPROVAL",
    result
)

print("Loan amount after attempted change:", customer.loan_amount)
print()


# ============================================================
# TEST 3 — REJECTED APPLICATION
# ============================================================

customer_rejected = CustomerCard(
    application_id="APP-LIFECYCLE-002",
    phone="+996TEST-LIFE-002",
)

rejected_messages = [
    "Это BYD Song Plus.",
    "2024 года.",
    "Примерная стоимость автомобиля 500 000 сом.",
    "400 000 сом.",
    "Автозалог, без передачи автомобиля.",
    "Я зарегистрирована в Бишкеке.",
]

for index, message in enumerate(
    rejected_messages,
    1
):

    result = process_conversation_message(
        customer_rejected,
        message
    )

    print_result(
        f"REJECTION TEST — TURN {index}",
        result
    )


print("=" * 60)
print("FINAL REJECTION")
print("=" * 60)
print("Stage:", customer_rejected.stage)
print("Decision:", customer_rejected.decision)
print("Loan amount:", customer_rejected.loan_amount)
print()


# ============================================================
# TEST 4 — MESSAGE AFTER REJECTION
# ============================================================

result = process_conversation_message(
    customer_rejected,
    "Тогда я хочу получить 100 000 сом."
)

print_result(
    "MESSAGE AFTER REJECTION",
    result
)

print(
    "Loan amount after attempted change:",
    customer_rejected.loan_amount
)
print()


print("=" * 60)
print("DECISION LIFECYCLE TEST COMPLETE")
print("=" * 60)
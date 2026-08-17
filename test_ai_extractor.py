# ============================================================
# AYLIN AI EXTRACTOR TEST
# Full-field deterministic test
# ============================================================

from ai_extractor import extract_information_with_ai


# ============================================================
# TEST CUSTOMER MESSAGE
# ============================================================

customer_message = """
Это BYD Song Plus, 2024 года.
Примерная стоимость автомобиля 1 500 000 сом.
Хотим получить 400 000 сом под автозалог, но без передачи автомобиля.
Я зарегистрирована в Бишкеке.
"""


# ============================================================
# RUN TEST
# ============================================================

print("=" * 60)
print("AYLIN AI EXTRACTOR TEST")
print("=" * 60)

print()
print("Customer message:")
print()
print(customer_message)

print()
print("AI extracted information:")
print("-" * 60)

result = extract_information_with_ai(customer_message)

for key, value in result.items():
    print(f"- {key}: {value}")

print("-" * 60)


# ============================================================
# EXPECTED RESULTS
# ============================================================

expected = {
    "car_model": "BYD Song Plus",
    "car_year": 2024,
    "car_value": 1500000.0,
    "loan_amount": 400000.0,
    "loan_program": "Автозалог",
    "registration_region": "Бишкеке",
}


# ============================================================
# VALIDATION
# ============================================================

print()
print("VALIDATION:")
print("-" * 60)

all_passed = True

for key, expected_value in expected.items():

    actual_value = result.get(key)

    if actual_value == expected_value:
        print(f"PASS  {key}: {actual_value}")
    else:
        print(
            f"FAIL  {key}: "
            f"expected={expected_value}, "
            f"actual={actual_value}"
        )
        all_passed = False


# ============================================================
# FINAL RESULT
# ============================================================

print("-" * 60)

if all_passed:
    print("ALL EXTRACTOR TESTS PASSED")
else:
    print("SOME EXTRACTOR TESTS FAILED")

print("=" * 60)
from customer_card import CustomerCard
from decision_engine import evaluate_application


# ============================================================
# TEST HELPER
# ============================================================

def create_customer(
    car_model="BYD Song Plus",
    car_year=2024,
    car_value=1_500_000.0,
    loan_amount=400_000.0,
    loan_program="Автозалог",
    registration_region="Бишкек"
):
    return CustomerCard(
        application_id="TEST-DECISION",
        phone="+996TEST001",
        car_model=car_model,
        car_year=car_year,
        car_value=car_value,
        loan_amount=loan_amount,
        loan_program=loan_program,
        registration_region=registration_region
    )


def print_result(name, customer, result):

    print("=" * 70)
    print(name)
    print("=" * 70)

    print()
    print("CUSTOMER")
    print("-" * 70)

    print(f"car_model: {customer.car_model}")
    print(f"car_year: {customer.car_year}")
    print(f"car_value: {customer.car_value}")
    print(f"loan_amount: {customer.loan_amount}")
    print(f"loan_program: {customer.loan_program}")
    print(f"registration_region: {customer.registration_region}")

    print()
    print("DECISION RESULT")
    print("-" * 70)

    print(f"decision: {result.get('decision')}")
    print(f"reason: {result.get('reason')}")
    print(f"loan_to_value: {result.get('loan_to_value')}")
    print(
        f"loan_to_value_percent: "
        f"{result.get('loan_to_value_percent')}"
    )
    print(f"errors: {result.get('errors')}")

    print()


# ============================================================
# TEST 1 — NORMAL APPLICATION
# ============================================================

def test_normal_application():

    customer = create_customer()

    result = evaluate_application(
        customer
    )

    print_result(
        "TEST 1 — NORMAL APPLICATION",
        customer,
        result
    )

    assert isinstance(
        result,
        dict
    )

    assert result.get(
        "decision"
    ) in (
        "approved",
        "rejected",
        "pending"
    )


# ============================================================
# TEST 2 — HIGH LOAN AMOUNT
# ============================================================

def test_high_loan_amount():

    customer = create_customer(
        car_value=1_000_000.0,
        loan_amount=900_000.0
    )

    result = evaluate_application(
        customer
    )

    print_result(
        "TEST 2 — HIGH LOAN AMOUNT",
        customer,
        result
    )

    assert isinstance(
        result,
        dict
    )

    assert result.get(
        "decision"
    ) in (
        "approved",
        "rejected",
        "pending"
    )


# ============================================================
# TEST 3 — LOW CAR VALUE
# ============================================================

def test_low_car_value():

    customer = create_customer(
        car_value=100_000.0,
        loan_amount=400_000.0
    )

    result = evaluate_application(
        customer
    )

    print_result(
        "TEST 3 — LOAN GREATER THAN CAR VALUE",
        customer,
        result
    )

    assert isinstance(
        result,
        dict
    )

    assert result.get(
        "decision"
    ) in (
        "approved",
        "rejected",
        "pending"
    )


# ============================================================
# TEST 4 — MISSING CAR VALUE
# ============================================================

def test_missing_car_value():

    customer = create_customer(
        car_value=None
    )

    result = evaluate_application(
        customer
    )

    print_result(
        "TEST 4 — MISSING CAR VALUE",
        customer,
        result
    )

    assert isinstance(
        result,
        dict
    )

    assert result.get(
        "decision"
    ) in (
        "approved",
        "rejected",
        "pending"
    )


# ============================================================
# TEST 5 — MISSING LOAN AMOUNT
# ============================================================

def test_missing_loan_amount():

    customer = create_customer(
        loan_amount=None
    )

    result = evaluate_application(
        customer
    )

    print_result(
        "TEST 5 — MISSING LOAN AMOUNT",
        customer,
        result
    )

    assert isinstance(
        result,
        dict
    )

    assert result.get(
        "decision"
    ) in (
        "approved",
        "rejected",
        "pending"
    )


# ============================================================
# TEST 6 — MISSING LOAN PROGRAM
# ============================================================

def test_missing_loan_program():

    customer = create_customer(
        loan_program=None
    )

    result = evaluate_application(
        customer
    )

    print_result(
        "TEST 6 — MISSING LOAN PROGRAM",
        customer,
        result
    )

    assert isinstance(
        result,
        dict
    )

    assert result.get(
        "decision"
    ) in (
        "approved",
        "rejected",
        "pending"
    )


# ============================================================
# TEST 7 — MISSING REGION
# ============================================================

def test_missing_region():

    customer = create_customer(
        registration_region=None
    )

    result = evaluate_application(
        customer
    )

    print_result(
        "TEST 7 — MISSING REGISTRATION REGION",
        customer,
        result
    )

    assert isinstance(
        result,
        dict
    )

    assert result.get(
        "decision"
    ) in (
        "approved",
        "rejected",
        "pending"
    )


# ============================================================
# RUN TESTS
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print("AYLIN DECISION ENGINE TEST SUITE")
    print("=" * 70)
    print()

    test_normal_application()

    test_high_loan_amount()

    test_low_car_value()

    test_missing_car_value()

    test_missing_loan_amount()

    test_missing_loan_program()

    test_missing_region()

    print("=" * 70)
    print("ALL DECISION ENGINE TESTS COMPLETED")
    print("=" * 70)

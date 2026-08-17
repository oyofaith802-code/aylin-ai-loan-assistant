from customer_card import CustomerCard
from application_pipeline import run_application_pipeline


def create_customer(
    application_id,
    phone,
    car_model="Toyota Camry",
    car_year=2021,
    car_value=1000000,
    loan_amount=300000,
    loan_program="Автозалог",
    vehicle_possession="customer",
    registration_region="Бишкек",
    loan_term_months=12
):

    customer = CustomerCard(
        application_id=application_id,
        phone=phone
    )

    customer.car_model = car_model
    customer.car_year = car_year
    customer.car_value = car_value

    customer.loan_amount = loan_amount
    customer.loan_program = loan_program

    customer.vehicle_possession = vehicle_possession
    customer.registration_region = registration_region

    customer.loan_term_months = loan_term_months

    return customer



def run_test(title, customer):

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    result = run_application_pipeline(customer)

    print(result)

    print("\nDecision:")
    print(
        result.get("decision", {})
        .get("decision")
    )

    print()



# =========================================================
# TEST 1: HIGH LTV
# =========================================================

customer = create_customer(
    application_id="TEST-LTV",
    phone="+996000000001",

    car_value=500000,
    loan_amount=450000
)

run_test(
    "TEST 1: LOAN TO VALUE TOO HIGH",
    customer
)



# =========================================================
# TEST 2: OLD VEHICLE
# =========================================================

customer = create_customer(
    application_id="TEST-OLD",
    phone="+996000000002",

    car_year=2005,
    car_value=1000000,
    loan_amount=300000
)

run_test(
    "TEST 2: OLD VEHICLE",
    customer
)



# =========================================================
# TEST 3: LOW LOAN AMOUNT
# =========================================================

customer = create_customer(
    application_id="TEST-MIN",
    phone="+996000000003",

    car_value=1000000,
    loan_amount=10000
)

run_test(
    "TEST 3: LOAN BELOW MINIMUM",
    customer
)



# =========================================================
# TEST 4: UNSUPPORTED PROGRAM
# =========================================================

customer = create_customer(
    application_id="TEST-PROGRAM",
    phone="+996000000004",

    loan_program="Ипотека"
)

run_test(
    "TEST 4: UNSUPPORTED LOAN PROGRAM",
    customer
)



# =========================================================
# TEST 5: MISSING INFORMATION
# =========================================================

customer = create_customer(
    application_id="TEST-MISSING",
    phone="+996000000005",

    car_value=None
)

run_test(
    "TEST 5: MISSING CAR VALUE",
    customer
)



print("=" * 60)
print("REJECTION SCENARIOS TEST FINISHED")
print("=" * 60)
from application_manager import (
    create_application,
    get_active_application,
    get_current_application,
    get_customer_application_history,
    start_new_application
)

from application_repository import (
    save_customer,
    save_decision
)


PHONE = "+996000000444"


print("=" * 60)
print("APPLICATION MANAGER TEST")
print("=" * 60)


# ============================================================
# 1. CREATE FIRST APPLICATION
# ============================================================

print("\n1. CREATE FIRST APPLICATION")

application_1 = create_application(
    PHONE
)

print(
    "Application ID:",
    application_1.application_id
)

print(
    "Phone:",
    application_1.phone
)

print(
    "Stage:",
    application_1.stage
)


# ============================================================
# 2. UPDATE FIRST APPLICATION
# ============================================================

print("\n2. UPDATE FIRST APPLICATION")

application_1.car_model = "Toyota Camry"
application_1.car_year = 2021
application_1.car_value = 1200000

application_1.loan_amount = 500000
application_1.loan_program = "Автозалог"

application_1.registration_region = "Бишкек"

application_1.stage = "approved"

save_customer(
    application_1
)

save_decision(
    application_1.application_id,
    "approved",
    "lender_policy_passed"
)

print(
    "First application:",
    application_1.application_id
)

print(
    "Stage:",
    application_1.stage
)


# ============================================================
# 3. CHECK ACTIVE APPLICATION
# ============================================================

print("\n3. CHECK ACTIVE APPLICATION")

active = get_active_application(
    PHONE
)

print(
    "Active application:",
    active
)


# ============================================================
# 4. START SECOND APPLICATION
# ============================================================

print("\n4. START SECOND APPLICATION")

application_2 = start_new_application(
    PHONE
)

print(
    "Second application:",
    application_2.application_id
)

print(
    "Stage:",
    application_2.stage
)


# ============================================================
# 5. CHECK ACTIVE APPLICATION AGAIN
# ============================================================

print("\n5. CHECK ACTIVE APPLICATION AGAIN")

active = get_active_application(
    PHONE
)

print(
    "Active application ID:",
    active.application_id
)

print(
    "Expected:",
    application_2.application_id
)


# ============================================================
# 6. APPLICATION HISTORY
# ============================================================

print("\n6. APPLICATION HISTORY")

history = get_customer_application_history(
    PHONE
)

for application in history:

    print("\n------------------------------")

    print(
        "ID:",
        application["application_id"]
    )

    print(
        "Car:",
        application["car_model"]
    )

    print(
        "Loan:",
        application["loan_amount"]
    )

    print(
        "Stage:",
        application["stage"]
    )

    print(
        "Decision:",
        application["decision"]
    )


# ============================================================
# 7. CURRENT APPLICATION
# ============================================================

print("\n7. CURRENT APPLICATION")

current = get_current_application(
    PHONE
)

print(
    "Current application:",
    current.application_id
)

print(
    "Stage:",
    current.stage
)


print("\n" + "=" * 60)
print("APPLICATION MANAGER TEST COMPLETE")
print("=" * 60)
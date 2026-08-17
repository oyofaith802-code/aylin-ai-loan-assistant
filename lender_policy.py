from customer_card import CustomerCard


# =========================================================
# CONFIGURABLE LENDER POLICY
# =========================================================

MAX_LOAN_TO_VALUE = 0.70

MIN_CAR_YEAR = 2010

MIN_LOAN_AMOUNT = 50_000

MAX_LOAN_AMOUNT = 5_000_000

SUPPORTED_LOAN_PROGRAMS = {
    "Автозалог",
    "Автозайм",
    "Без изъятия автомобиля",
    "С размещением автомобиля на охраняемой стоянке",
}


# =========================================================
# EVALUATE LENDER POLICY
# =========================================================

def evaluate_lender_policy(
    customer: CustomerCard
) -> dict:
    """
    Perform a preliminary eligibility check.

    This function evaluates the application against
    configurable business rules.

    It does NOT perform a final legal/credit decision.
    """

    errors = []
    warnings = []

    # =====================================================
    # REQUIRED INFORMATION
    # =====================================================

    if customer.car_value is None:
        errors.append("car_value_missing")

    if customer.loan_amount is None:
        errors.append("loan_amount_missing")

    if customer.car_year is None:
        errors.append("car_year_missing")

    if not customer.loan_program:
        errors.append("loan_program_missing")

    if not customer.registration_region:
        errors.append("registration_region_missing")

    if customer.loan_term_months is None:
        errors.append("loan_term_months_missing")

    # =====================================================
    # STOP IF REQUIRED DATA IS MISSING
    # =====================================================

    if errors:
        return {
            "eligible": False,
            "decision": "pending",
            "reason": "required_information_missing",
            "errors": errors,
            "warnings": warnings,
        }

    # =====================================================
    # NUMERIC VALIDATION
    # =====================================================

    try:
        car_value = float(customer.car_value)
    except (TypeError, ValueError):
        errors.append("invalid_car_value")
        car_value = None

    try:
        loan_amount = float(customer.loan_amount)
    except (TypeError, ValueError):
        errors.append("invalid_loan_amount")
        loan_amount = None

    try:
        car_year = int(customer.car_year)
    except (TypeError, ValueError):
        errors.append("invalid_car_year")
        car_year = None

    # =====================================================
    # STOP IF NUMERIC VALUES ARE INVALID
    # =====================================================

    if errors:
        return {
            "eligible": False,
            "decision": "pending",
            "reason": "invalid_application_data",
            "errors": errors,
            "warnings": warnings,
        }

    # =====================================================
    # VEHICLE VALUE
    # =====================================================

    if car_value <= 0:
        errors.append("car_value_invalid")

    # =====================================================
    # LOAN AMOUNT
    # =====================================================

    if loan_amount <= 0:
        errors.append("loan_amount_invalid")

    elif loan_amount < MIN_LOAN_AMOUNT:
        errors.append("loan_amount_below_minimum")

    elif loan_amount > MAX_LOAN_AMOUNT:
        errors.append("loan_amount_above_maximum")

    # =====================================================
    # VEHICLE YEAR
    # =====================================================

    if car_year < MIN_CAR_YEAR:
        errors.append("vehicle_too_old")

    # =====================================================
    # LOAN PROGRAM
    # =====================================================

    if customer.loan_program not in SUPPORTED_LOAN_PROGRAMS:
        errors.append("unsupported_loan_program")

    # =====================================================
    # VEHICLE POSSESSION
    # =====================================================

    # At this stage we don't automatically reject either
    # possession model. The actual lender policy should
    # determine whether customer-retained vehicles are
    # supported for a specific program.

    if customer.vehicle_possession == "customer":
        warnings.append(
            "vehicle_remains_with_customer"
        )

    elif customer.vehicle_possession == "lender":
        warnings.append(
            "vehicle_transferred_to_lender"
        )

    # Unknown possession status is not treated as approval
    # evidence.
    elif customer.vehicle_possession is not None:
        warnings.append(
            "vehicle_possession_unknown"
        )

    # =====================================================
    # LOAN-TO-VALUE
    # =====================================================

    loan_to_value = None
    loan_to_value_percent = None

    if car_value > 0 and loan_amount > 0:

        loan_to_value = (
            loan_amount / car_value
        )

        loan_to_value_percent = (
            loan_to_value * 100
        )

        if loan_to_value > MAX_LOAN_TO_VALUE:
            errors.append(
                "loan_to_value_exceeds_limit"
            )

    # =====================================================
    # POLICY FAILURE
    # =====================================================

    if errors:

        result = {
            "eligible": False,
            "decision": "rejected",
            "reason": "lender_policy_failed",
            "errors": errors,
            "warnings": warnings,
        }

        if loan_to_value is not None:
            result["loan_to_value"] = round(
                loan_to_value,
                4
            )

            result["loan_to_value_percent"] = round(
                loan_to_value_percent,
                2
            )

        return result

    # =====================================================
    # PRELIMINARILY ELIGIBLE
    # =====================================================

    return {
        "eligible": True,
        "decision": "approved",
        "reason": "lender_policy_passed",
        "errors": [],
        "warnings": warnings,
        "loan_to_value": round(
            loan_to_value,
            4
        ),
        "loan_to_value_percent": round(
            loan_to_value_percent,
            2
        ),
    }
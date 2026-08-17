# validation.py

from __future__ import annotations

from typing import Any, Dict, List, Optional


# ============================================================
# REQUIRED APPLICATION FIELDS
# ============================================================

REQUIRED_FIELDS = [
    "car_model",
    "car_year",
    "car_value",
    "loan_amount",
    "loan_program",
    "registration_region",
]


# ============================================================
# HELPERS
# ============================================================

def _is_missing(
    value: Any,
) -> bool:

    return (
        value is None
        or value == ""
    )


# ============================================================
# BASIC VALIDATORS
# ============================================================

def validate_car_year(
    year: Any,
) -> bool:

    if year is None:
        return False

    try:
        year = int(year)
    except (
        ValueError,
        TypeError,
    ):
        return False

    return 1980 <= year <= 2035


def validate_positive_number(
    value: Any,
) -> bool:

    if value is None:
        return False

    try:
        return float(value) > 0
    except (
        ValueError,
        TypeError,
    ):
        return False


def validate_loan_to_value(
    loan_amount: Optional[float],
    car_value: Optional[float],
    max_ltv: float = 0.70,
) -> bool:

    if not validate_positive_number(
        loan_amount
    ):
        return False

    if not validate_positive_number(
        car_value
    ):
        return False

    return (
        float(loan_amount)
        / float(car_value)
        <= max_ltv
    )


# ============================================================
# FIELD VALIDATOR
# ============================================================

def validate_field(
    field: str,
    value: Any,
) -> bool:

    if field in {
        "car_value",
        "loan_amount",
    }:

        return validate_positive_number(
            value
        )

    if field == "car_year":

        return validate_car_year(
            value
        )

    if field in {
        "car_model",
        "loan_program",
        "registration_region",
    }:

        return not _is_missing(
            value
        )

    if field == "loan_term_months":

        if value is None:
            return False

        try:
            value = int(value)
        except (
            ValueError,
            TypeError,
        ):
            return False

        return 1 <= value <= 60

    return True


# ============================================================
# VALIDATE CURRENT MESSAGE EXTRACTION
# ============================================================

def validate_extraction(
    extracted: Dict[str, Any],
) -> Dict[str, Any]:

    """
    Validates ONLY the information extracted from the
    current customer message.

    Missing values are allowed.

    A missing value is returned as None.

    Valid values are preserved.
    """

    cleaned: Dict[str, Any] = {}

    errors: List[Dict[str, Any]] = []

    fields = [
        "car_model",
        "car_year",
        "car_value",
        "loan_amount",
        "loan_program",
        "registration_region",
        "loan_term_months",
    ]

    for field in fields:

        value = extracted.get(
            field
        )

        # ----------------------------------------------------
        # Missing from current message
        # ----------------------------------------------------

        if value is None:

            cleaned[field] = None

            continue

        # ----------------------------------------------------
        # Normalize integer fields
        # ----------------------------------------------------

        if field in {
            "car_year",
            "loan_term_months",
        }:

            try:
                value = int(value)

            except (
                ValueError,
                TypeError,
            ):

                cleaned[field] = None

                errors.append({
                    "type": "invalid_field",
                    "field": field,
                    "value": value,
                })

                continue

        # ----------------------------------------------------
        # Normalize numeric fields
        # ----------------------------------------------------

        if field in {
            "car_value",
            "loan_amount",
        }:

            try:
                value = float(value)

            except (
                ValueError,
                TypeError,
            ):

                cleaned[field] = None

                errors.append({
                    "type": "invalid_field",
                    "field": field,
                    "value": value,
                })

                continue

        # ----------------------------------------------------
        # Validate
        # ----------------------------------------------------

        if not validate_field(
            field,
            value,
        ):

            cleaned[field] = None

            errors.append({
                "type": "invalid_field",
                "field": field,
                "value": value,
            })

            continue

        # ----------------------------------------------------
        # Valid value
        # ----------------------------------------------------

        cleaned[field] = value

    return {
        "valid": len(errors) == 0,
        "cleaned": cleaned,
        "errors": errors,
    }


# ============================================================
# MISSING APPLICATION FIELDS
# ============================================================

def get_missing_fields(
    card: Dict[str, Any],
) -> List[str]:

    missing = []

    for field in REQUIRED_FIELDS:

        value = card.get(
            field
        )

        if _is_missing(value):
            missing.append(field)

    return missing


# ============================================================
# COMPATIBILITY NAME
# ============================================================

def get_missing_required_fields(
    card: Dict[str, Any],
) -> List[str]:

    return get_missing_fields(
        card
    )


# ============================================================
# FULL APPLICATION VALIDATION
# ============================================================

def validate_application(
    card: Dict[str, Any],
) -> Dict[str, Any]:

    errors: List[Dict[str, Any]] = []

    # --------------------------------------------------------
    # Required fields
    # --------------------------------------------------------

    missing_fields = get_missing_fields(
        card
    )

    if missing_fields:

        errors.append({
            "type": "missing_fields",
            "fields": missing_fields,
        })

    # --------------------------------------------------------
    # Field validation
    # --------------------------------------------------------

    for field in REQUIRED_FIELDS:

        value = card.get(
            field
        )

        if (
            value is not None
            and not validate_field(
                field,
                value,
            )
        ):

            errors.append({
                "type": "invalid_field",
                "field": field,
                "value": value,
            })

    # --------------------------------------------------------
    # Loan / car value
    # --------------------------------------------------------

    loan_amount = card.get(
        "loan_amount"
    )

    car_value = card.get(
        "car_value"
    )

    if (
        validate_positive_number(
            loan_amount
        )
        and validate_positive_number(
            car_value
        )
    ):

        loan_amount = float(
            loan_amount
        )

        car_value = float(
            car_value
        )

        # Loan cannot exceed car value
        if loan_amount > car_value:

            errors.append({
                "type": "loan_exceeds_car_value",
                "loan_amount": loan_amount,
                "car_value": car_value,
            })

    # --------------------------------------------------------
    # LTV
    # --------------------------------------------------------

    ltv = None
    ltv_percent = None

    if (
        validate_positive_number(
            loan_amount
        )
        and validate_positive_number(
            car_value
        )
    ):

        ltv = (
            float(loan_amount)
            / float(car_value)
        )

        ltv_percent = round(
            ltv * 100,
            2,
        )

        if ltv > 0.70:

            errors.append({
                "type": "ltv_too_high",
                "loan_to_value": round(
                    ltv,
                    4,
                ),
                "loan_to_value_percent": ltv_percent,
                "max_ltv_percent": 70.0,
            })

    # --------------------------------------------------------
    # Result
    # --------------------------------------------------------

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "missing_fields": missing_fields,
        "loan_to_value": (
            round(
                ltv,
                4,
            )
            if ltv is not None
            else None
        ),
        "loan_to_value_percent": ltv_percent,
    }


# ============================================================
# DECISION CHECK
# ============================================================

def can_make_decision(
    card: Dict[str, Any],
) -> bool:

    result = validate_application(
        card
    )

    return (
        result["valid"]
        and not result["missing_fields"]
    )


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

validate = validate_application

validate_fields = validate_application

is_valid_application = can_make_decision


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    extracted = {
        "car_model": None,
        "car_year": None,
        "car_value": None,
        "loan_amount": 400000.0,
        "loan_program": None,
        "registration_region": None,
        "loan_term_months": 1,
    }

    print("=" * 60)
    print("EXTRACTION VALIDATION")
    print("=" * 60)

    print(
        validate_extraction(
            extracted
        )
    )

    card = {
        "car_model": "BYD Song Plus",
        "car_year": 2024,
        "car_value": 1_500_000,
        "loan_amount": 400_000,
        "loan_program": "Автозалог",
        "registration_region": "Бишкеке",
    }

    print()
    print("=" * 60)
    print("APPLICATION VALIDATION")
    print("=" * 60)

    print(
        validate_application(
            card
        )
    )
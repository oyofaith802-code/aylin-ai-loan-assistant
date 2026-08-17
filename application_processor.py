from customer_card import CustomerCard
from application_validator import validate_application


def process_application(customer: CustomerCard) -> dict:
    """
    Process a completed loan application.

    The application is validated before it can proceed.
    This function does not make the business decision.
    """

    # ---------------------------------------------------------
    # 1. Validate application
    # ---------------------------------------------------------

    validation = validate_application(customer)

    if not validation["valid"]:
        return {
            "status": "validation_failed",
            "errors": validation["errors"]
        }

    # ---------------------------------------------------------
    # 2. Build structured application
    # ---------------------------------------------------------

    application = {
        "application_id": customer.application_id,
        "phone": customer.phone,

        "car": {
            "model": customer.car_model,
            "year": customer.car_year,
            "value": customer.car_value,
        },

        "loan": {
            "amount": customer.loan_amount,
            "program": customer.loan_program,
            "term_months": customer.loan_term_months,
        },

        "vehicle": {
            "possession": customer.vehicle_possession,
        },

        "customer": {
            "registration_region": customer.registration_region,
        },

        "stage": "processing_application",
    }

    # ---------------------------------------------------------
    # 3. Return validated application
    # ---------------------------------------------------------

    return {
        "status": "ready_for_processing",
        "application": application
    }
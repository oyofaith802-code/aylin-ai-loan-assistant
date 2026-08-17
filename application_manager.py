from uuid import uuid4

from customer_card import CustomerCard

from application_repository import (
    get_application,
    get_application_by_phone,
    get_applications_by_phone,
    save_customer,
)


# ============================================================
# APPLICATION ID
# ============================================================

def generate_application_id() -> str:
    """
    Generate a unique application ID.
    """
    return f"APP-{uuid4().hex[:12].upper()}"


# ============================================================
# CREATE APPLICATION
# ============================================================

def create_application(phone: str) -> CustomerCard:
    """
    Create a completely new application.
    """

    application_id = generate_application_id()

    customer = CustomerCard(
        application_id=application_id,
        phone=phone,
        stage="new"
    )

    save_customer(customer)

    return customer


# ============================================================
# LOAD APPLICATION
# ============================================================

def load_application(
    application_id: str
) -> CustomerCard | None:
    """
    Load an application from the database
    and convert it into a CustomerCard.
    """

    application = get_application(
        application_id
    )

    if application is None:
        return None

    return CustomerCard(
        # ----------------------------------------------------
        # APPLICATION
        # ----------------------------------------------------

        application_id=application.application_id,

        phone=application.phone,

        # ----------------------------------------------------
        # VEHICLE
        # ----------------------------------------------------

        car_model=application.car_model,

        car_year=application.car_year,

        car_value=application.car_value,

        # ----------------------------------------------------
        # LOAN
        # ----------------------------------------------------

        loan_amount=application.loan_amount,

        loan_program=application.loan_program,

        # ----------------------------------------------------
        # CUSTOMER
        # ----------------------------------------------------

        registration_region=(
            application.registration_region
        ),

        # ----------------------------------------------------
        # APPLICATION STATE
        # ----------------------------------------------------

        stage=application.stage,

        # ----------------------------------------------------
        # BUSINESS DECISION
        # ----------------------------------------------------

        decision=application.decision,

        decision_reason=(
            application.decision_reason
        )
    )


# ============================================================
# GET ACTIVE APPLICATION
# ============================================================

def get_active_application(
    phone: str
) -> CustomerCard | None:
    """
    Return the customer's currently active application.

    Completed/approved/rejected applications are not
    considered active.
    """

    applications = get_applications_by_phone(
        phone
    )

    for application in applications:

        if application.stage not in (
            "approved",
            "rejected",
            "completed"
        ):

            return load_application(
                application.application_id
            )

    return None


# ============================================================
# GET CURRENT APPLICATION
# ============================================================

def get_current_application(
    phone: str
) -> CustomerCard | None:
    """
    Return the active application.

    If there is no active application, return
    the customer's latest application.
    """

    active = get_active_application(
        phone
    )

    if active is not None:
        return active

    latest = get_application_by_phone(
        phone
    )

    if latest is None:
        return None

    return load_application(
        latest.application_id
    )


# ============================================================
# APPLICATION HISTORY
# ============================================================

def get_customer_application_history(
    phone: str
) -> list[dict]:
    """
    Return all applications belonging to a customer.
    """

    applications = get_applications_by_phone(
        phone
    )

    result = []

    for application in applications:

        result.append({

            "application_id":
                application.application_id,

            "phone":
                application.phone,

            "car_model":
                application.car_model,

            "car_year":
                application.car_year,

            "car_value":
                application.car_value,

            "loan_amount":
                application.loan_amount,

            "loan_program":
                application.loan_program,

            "registration_region":
                application.registration_region,

            "stage":
                application.stage,

            "decision":
                application.decision,

            "decision_reason":
                application.decision_reason,

            "created_at":
                application.created_at,

            "updated_at":
                application.updated_at
        })

    return result


# ============================================================
# START NEW APPLICATION
# ============================================================

def start_new_application(
    phone: str
) -> CustomerCard:
    """
    Explicitly start a completely new application.

    This does NOT reuse an existing application.
    """

    return create_application(
        phone
    )
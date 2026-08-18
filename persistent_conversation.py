from uuid import uuid4

from customer_card import CustomerCard

from application_repository import (
    create_application_table,
    get_application,
    get_applications_by_phone,
    save_customer,
    save_decision,
    save_conversation_message,
)

from conversation_application import (
    process_conversation_message
)


# ============================================================
# APPLICATION ID
# ============================================================

def generate_application_id() -> str:
    return f"APP-{uuid4().hex[:12].upper()}"


# ============================================================
# ACTIVE APPLICATION STATES
# ============================================================

FINAL_STAGES = {
    "approved",
    "rejected",
    "completed",
}


# ============================================================
# CONVERT DATABASE APPLICATION TO CUSTOMER CARD
# ============================================================

def application_to_customer_card(
    application
) -> CustomerCard:

    return CustomerCard(
        application_id=application.application_id,
        phone=application.phone,

        car_model=application.car_model,
        car_year=application.car_year,
        car_value=application.car_value,

        loan_amount=application.loan_amount,
        loan_program=application.loan_program,

        loan_term_months=getattr(
            application,
            "loan_term_months",
            None
        ),

        vehicle_possession=getattr(
            application,
            "vehicle_possession",
            None
        ),

        registration_region=(
            application.registration_region
        ),

        stage=application.stage,

        introduced=bool(
            getattr(
                application,
                "introduced",
                0
            )
        ),

        decision=getattr(
            application,
            "decision",
            None
        ),

        decision_reason=getattr(
            application,
            "decision_reason",
            None
        )
    )


# ============================================================
# FIND ACTIVE APPLICATION
# ============================================================

def get_active_customer_application(
    phone: str
):

    applications = get_applications_by_phone(
        phone
    )

    for application in applications:

        if application.stage not in FINAL_STAGES:

            return application_to_customer_card(
                application
            )

    return None


# ============================================================
# LOAD OR CREATE CUSTOMER
# ============================================================

def load_or_create_customer(
    phone: str,
    application_id: str | None = None
):

    # --------------------------------------------------------
    # 1. Explicit application ID
    # --------------------------------------------------------

    if application_id:

        existing = get_application(
            application_id
        )

        if existing is not None:

            # Prevent accidentally using another
            # customer's application ID.
            if existing.phone != phone:

                raise ValueError(
                    "Application does not belong to this phone number"
                )

            return application_to_customer_card(
                existing
            )

    # --------------------------------------------------------
    # 2. Find ACTIVE application
    # --------------------------------------------------------

    active = get_active_customer_application(
        phone
    )

    if active is not None:

        # ----------------------------------------------------
        # Restore known customer information from the most
        # recent previous application.
        #
        # A new/active application should not forget vehicle,
        # loan, possession, or registration information that
        # was already collected from this customer.
        # ----------------------------------------------------

        applications = get_applications_by_phone(
            phone
        )

        previous = None

        for application in applications:

            if application.application_id == active.application_id:
                continue

            if application.stage in FINAL_STAGES:
                previous = application
                break

        if previous is not None:

            fields_to_restore = (
                "car_model",
                "car_year",
                "car_value",
                "loan_amount",
                "loan_program",
                "vehicle_possession",
                "registration_region",
                "loan_term_months",
            )

            changed = False

            for field_name in fields_to_restore:

                current_value = getattr(
                    active,
                    field_name,
                    None
                )

                previous_value = getattr(
                    previous,
                    field_name,
                    None
                )

                if (
                    current_value is None
                    and previous_value is not None
                ):

                    setattr(
                        active,
                        field_name,
                        previous_value
                    )

                    changed = True

            if changed:

                save_customer(
                    active
                )

        return active

    # --------------------------------------------------------
    # 3. No active application exists
    #
    # Create a completely new application.
    # --------------------------------------------------------

    customer = CustomerCard(
        application_id=generate_application_id(),
        phone=phone,
        stage="new"
    )

    save_customer(
        customer
    )

    return customer


# ============================================================
# PROCESS PERSISTENT MESSAGE
# ============================================================

def process_persistent_message(
    phone: str,
    message: str,
    application_id: str | None = None
) -> dict:

    # --------------------------------------------------------
    # Make sure database table exists
    # --------------------------------------------------------

    create_application_table()

    # --------------------------------------------------------
    # Load existing active application
    # or create a new one
    # --------------------------------------------------------

    customer = load_or_create_customer(
        phone=phone,
        application_id=application_id
    )

    # --------------------------------------------------------
    # If a decision already exists, do not run the
    # application pipeline again.
    # --------------------------------------------------------

    if customer.decision in (
        "approved",
        "rejected"
    ):

        return {
            "application_id":
                customer.application_id,

            "status":
                "decision_already_made",

            "response":
                (
                    "Ваша заявка уже была "
                    "предварительно одобрена."
                    if customer.decision == "approved"
                    else
                    "По вашей заявке уже было "
                    "принято решение."
                ),

            "stage":
                customer.stage,

            "decision":
                customer.decision,

            "decision_reason":
                customer.decision_reason,

            "next_field":
                None,

            "errors":
                []
        }

    # --------------------------------------------------------
    # Save customer message
    # --------------------------------------------------------

    save_conversation_message(
        application_id=customer.application_id,
        phone=customer.phone,
        sender="customer",
        message=message
    )

    # --------------------------------------------------------
    # Process customer message
    # --------------------------------------------------------

    result = process_conversation_message(
        customer,
        message
    )

    # --------------------------------------------------------
    # Synchronize result with CustomerCard
    # --------------------------------------------------------

    result_stage = result.get(
        "stage"
    )

    if result_stage:

        customer.stage = result_stage

    decision = result.get(
        "decision"
    )

    if decision:

        customer.decision = decision.get(
            "decision"
        )

        customer.decision_reason = decision.get(
            "reason"
        )

    # --------------------------------------------------------
    # Save current application state
    # --------------------------------------------------------

    save_customer(
        customer
    )

    # --------------------------------------------------------
    # Save decision explicitly
    # --------------------------------------------------------

    if decision:

        decision_name = decision.get(
            "decision"
        )

        reason = decision.get(
            "reason",
            ""
        )

        if decision_name:

            save_decision(
                customer.application_id,
                decision_name,
                reason
            )

    # --------------------------------------------------------
    # Save Aylin response
    # --------------------------------------------------------

    response_text = result.get(
        "response"
    )

    # --------------------------------------------------------
    # FIRST-CONTACT INTRODUCTION
    # --------------------------------------------------------
    #
    # Aylin introduces herself only once.
    #
    # The application pipeline still processes the customer's
    # first message normally, so information supplied in that
    # first message is not lost.
    # --------------------------------------------------------

    if not customer.introduced:

        introduction = (
            "Здравствуйте! Я Айлин, менеджер "
            "автоломбарда «Молодой». "
            "Готова помочь Вам с оформлением займа."
        )

        if response_text:

            response_text = (
                introduction
                + "\n\n"
                + response_text
            )

        else:

            response_text = introduction

        customer.introduced = True

        # Persist the flag immediately so a reload does not
        # introduce Aylin again.
        save_customer(
            customer
        )

    if response_text:
        save_conversation_message(
            application_id=customer.application_id,
            phone=customer.phone,
            sender="aylin",
            message=response_text
        )

    # --------------------------------------------------------
    # Return complete API result
    # --------------------------------------------------------

    return {
        "application_id":
            customer.application_id,

        "phone":
            customer.phone,

        "customer":
            customer,

        "status":
            result.get(
                "status"
            ),

        "response":
            result.get(
                "response"
            ),

        "stage":
            customer.stage,

        "decision":
            customer.decision,

        "decision_reason":
            customer.decision_reason,

        "next_field":
            result.get(
                "next_field"
            ),

        "application":
            result.get(
                "application"
            ),

        "business_evaluation":
            result.get(
                "business_evaluation"
            ),

        "errors":
            result.get(
                "errors",
                []
            )
    }


# ============================================================
# START NEW APPLICATION
# ============================================================

def start_persistent_application(
    phone: str
) -> CustomerCard:

    customer = CustomerCard(
        application_id=generate_application_id(),
        phone=phone,
        stage="new"
    )

    save_customer(
        customer
    )

    return customer

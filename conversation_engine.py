from customer_card import CustomerCard

from ai_card_updater import (
    update_customer_card_from_message
)

from stage_flow import (
    process_information_stage
)

from application_pipeline import (
    run_application_pipeline
)

from decision_response import (
    generate_decision_response
)


def process_customer_message(
    customer: CustomerCard,
    message: str
):
    """
    Main Aylin conversation engine.

    Flow:

        Customer message
              ↓
        AI extraction
              ↓
        CustomerCard update
              ↓
        Information collection
              ↓
        Application pipeline
              ↓
        Business decision
              ↓
        Customer response
    """

    # ========================================================
    # 0. CLEAN MESSAGE
    # ========================================================

    message = message.strip()

    if not message:

        return {
            "status": "error",
            "response": "Пожалуйста, напишите ваш вопрос.",
            "next_field": None,
            "stage": getattr(
                customer,
                "stage",
                None
            ),
        }

    # ========================================================
    # 1. EXTRACT + MERGE CUSTOMER INFORMATION
    # ========================================================

    extracted = update_customer_card_from_message(
        customer,
        message
    )

    # ========================================================
    # 2. PROCESS INFORMATION COLLECTION
    # ========================================================

    stage_result = process_information_stage(
        customer
    )

    # ========================================================
    # 3. INFORMATION STILL MISSING
    # ========================================================

    if stage_result["status"] == "waiting_for_customer":

        return {
            "status": "waiting_for_customer",

            "response": stage_result.get(
                "question"
            ),

            "next_field": stage_result.get(
                "next_field"
            ),

            "stage": getattr(
                customer,
                "stage",
                None
            ),

            "extracted": extracted,
        }

    # ========================================================
    # 4. INFORMATION COMPLETE
    # ========================================================

    if stage_result["status"] == "information_complete":

        # ----------------------------------------------------
        # Run the actual application pipeline
        # ----------------------------------------------------

        pipeline_result = run_application_pipeline(
            customer
        )

        # ----------------------------------------------------
        # Pipeline failed validation
        # ----------------------------------------------------

        if pipeline_result["status"] != "decision_ready":

            return {
                "status": pipeline_result["status"],

                "response": (
                    "Не удалось продолжить обработку заявки. "
                    "Пожалуйста, проверьте предоставленную информацию."
                ),

                "next_field": None,

                "stage": getattr(
                    customer,
                    "stage",
                    None
                ),

                "errors": pipeline_result.get(
                    "errors",
                    []
                ),

                "extracted": extracted,
            }

        # ----------------------------------------------------
        # Get business decision
        # ----------------------------------------------------

        decision_result = pipeline_result.get(
            "decision",
            {}
        )

        # ----------------------------------------------------
        # Generate customer-friendly response
        # ----------------------------------------------------

        response = generate_decision_response(
            decision_result,
            customer
        )

        # ----------------------------------------------------
        # Return complete result
        # ----------------------------------------------------

        return {
            "status": "decision_ready",

            "response": response,

            "next_field": None,

            "stage": getattr(
                customer,
                "stage",
                None
            ),

            "decision": decision_result,

            "business_evaluation":
                pipeline_result.get(
                    "business_evaluation"
                ),

            "application":
                pipeline_result.get(
                    "application"
                ),

            "extracted": extracted,
        }

    # ========================================================
    # 5. FALLBACK
    # ========================================================

    return {
        "status": "unknown",

        "response":
            "Пожалуйста, уточните ваш вопрос.",

        "next_field": None,

        "stage": getattr(
            customer,
            "stage",
            None
        ),

        "extracted": extracted,
    }
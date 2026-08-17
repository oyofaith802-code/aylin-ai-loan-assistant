from customer_card import CustomerCard
from stages import ApplicationStage
from application_state import (
    transition_stage,
    transition_after_decision
)
from application_processor import process_application
from lender_policy import evaluate_lender_policy
from decision_engine import make_business_decision


def run_application_pipeline(
    customer: CustomerCard
) -> dict:
    """
    Run the complete application pipeline.
    """

    # =========================================================
    # 1. Move to processing
    # =========================================================

    transition_stage(
        customer,
        ApplicationStage.PROCESSING_APPLICATION
    )

    # =========================================================
    # 2. Validate + process
    # =========================================================

    processing_result = process_application(
        customer
    )

    if processing_result["status"] != "ready_for_processing":

        return {
            "status": processing_result["status"],
            "errors": processing_result.get(
                "errors",
                []
            ),
            "stage": customer.stage
        }

    # =========================================================
    # 3. Move to business decision
    # =========================================================

    transition_stage(
        customer,
        ApplicationStage.BUSINESS_DECISION
    )

    processing_result["application"]["stage"] = (
        customer.stage
    )

    # =========================================================
    # 4. Lender policy
    # =========================================================

    policy_result = evaluate_lender_policy(
        customer
    )

    # =========================================================
    # 5. Decision engine
    # =========================================================

    decision_result = make_business_decision(
        customer
    )

    # =========================================================
    # 6. Update application stage
    # =========================================================

    decision = decision_result["decision"]

    transition_after_decision(
        customer,
        decision
    )

    # Keep application snapshot synchronized
    processing_result["application"]["stage"] = (
        customer.stage
    )

    # =========================================================
    # 7. Final result
    # =========================================================

    return {
        "status": "decision_ready",
        "stage": customer.stage,
        "application": processing_result[
            "application"
        ],
        "business_evaluation": policy_result,
        "decision": decision_result
    }
from customer_card import CustomerCard
from stage_flow import process_information_stage


def process_stage(customer: CustomerCard) -> dict:
    """
    Manage the current Aylin application stage.
    """

    result = process_information_stage(customer)

    # ---------------------------------------------------------
    # Still collecting information
    # ---------------------------------------------------------

    if result["status"] == "waiting_for_customer":

        customer.stage = "collecting_information"

        return {
            "stage": "collecting_information",
            "status": "waiting_for_customer",
            "question": result["question"]
        }

    # ---------------------------------------------------------
    # Information collection completed
    # ---------------------------------------------------------

    if result["status"] == "information_complete":

        customer.stage = "processing_application"

        return {
            "stage": "processing_application",
            "status": "stage_completed",
            "question": None
        }

    return result

# ============================================================
# COMPATIBILITY API
# ============================================================

def set_stage(
    customer: CustomerCard,
    stage
) -> CustomerCard:
    """
    Compatibility wrapper for older stage-manager tests.

    The canonical storage remains customer.stage.
    """

    if hasattr(stage, "value"):
        customer.stage = stage.value
    else:
        customer.stage = str(stage)

    return customer


def get_stage(
    customer: CustomerCard
) -> str:
    """
    Return the current application stage.
    """

    return customer.stage

from customer_card import CustomerCard

from lender_policy import evaluate_lender_policy


# =========================================================
# BUSINESS DECISION
# =========================================================

def make_business_decision(
    customer: CustomerCard
) -> dict:
    """
    Make the business decision using the lender policy.

    Possible decisions:

        approved
        rejected
        pending
    """

    policy_result = evaluate_lender_policy(customer)

    # ---------------------------------------------------------
    # Safety check
    # ---------------------------------------------------------

    if not isinstance(policy_result, dict):
        return {
            "decision": "pending",
            "reason": "invalid_policy_result",
            "errors": [
                "Lender policy returned an invalid result."
            ],
            "warnings": [],
        }

    decision = policy_result.get("decision")

    # ---------------------------------------------------------
    # Normalize unexpected decision
    # ---------------------------------------------------------

    if decision not in {
        "approved",
        "rejected",
        "pending",
    }:
        return {
            "decision": "pending",
            "reason": "invalid_policy_decision",
            "errors": [
                "Unknown lender policy decision."
            ],
            "warnings": policy_result.get(
                "warnings",
                []
            ),
        }

    # ---------------------------------------------------------
    # Final result
    # ---------------------------------------------------------

    return {
        "decision": decision,
        "reason": policy_result.get(
            "reason",
            f"lender_policy_{decision}"
        ),
        "errors": policy_result.get(
            "errors",
            []
        ),
        "warnings": policy_result.get(
            "warnings",
            []
        ),
        "loan_to_value": policy_result.get(
            "loan_to_value"
        ),
        "loan_to_value_percent": policy_result.get(
            "loan_to_value_percent"
        ),
    }


# =========================================================
# BACKWARD COMPATIBILITY
# =========================================================

def evaluate_application(
    customer: CustomerCard
) -> dict:
    """
    Backward-compatible wrapper.

    Existing tests or modules using evaluate_application()
    can continue working.
    """

    return make_business_decision(customer)
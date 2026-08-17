from customer_card import CustomerCard
from lender_policy import evaluate_lender_policy


def make_business_decision(
    customer: CustomerCard
) -> dict:
    """
    Make the final business decision using
    the lender policy.
    """

    # ---------------------------------------------------------
    # Evaluate lender policy
    # ---------------------------------------------------------

    policy_result = evaluate_lender_policy(
        customer
    )

    # ---------------------------------------------------------
    # Policy rejected the application
    # ---------------------------------------------------------

    if not policy_result["eligible"]:

        return {
            "decision": "rejected",
            "reason": "lender_policy_failed",
            "errors": policy_result["errors"],
            "loan_to_value":
                policy_result.get(
                    "loan_to_value"
                ),
            "loan_to_value_percent":
                policy_result.get(
                    "loan_to_value_percent"
                )
        }

    # ---------------------------------------------------------
    # Policy approved the application
    # ---------------------------------------------------------

    return {
        "decision": "approved",
        "reason": "lender_policy_passed",
        "loan_to_value":
            policy_result["loan_to_value"],
        "loan_to_value_percent":
            policy_result["loan_to_value_percent"]
    }
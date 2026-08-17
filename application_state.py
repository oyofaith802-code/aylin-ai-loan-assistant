from customer_card import CustomerCard
from stages import ApplicationStage


def transition_stage(
    customer: CustomerCard,
    stage: ApplicationStage
) -> CustomerCard:
    """
    Move the customer application to a new stage.
    """

    customer.stage = stage.value

    return customer


def transition_after_decision(
    customer: CustomerCard,
    decision: str
) -> CustomerCard:
    """
    Move the application to the correct stage
    after a business decision.
    """

    if decision == "approved":

        transition_stage(
            customer,
            ApplicationStage.APPROVED
        )

    elif decision == "rejected":

        transition_stage(
            customer,
            ApplicationStage.REJECTED
        )

    elif decision == "manual_review":

        transition_stage(
            customer,
            ApplicationStage.MANUAL_REVIEW
        )

    return customer
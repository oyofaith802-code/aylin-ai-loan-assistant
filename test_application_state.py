from customer_card import CustomerCard
from stages import ApplicationStage
from application_state import transition_stage, transition_after_decision


def test_transition_stage_updates_customer_stage():

    customer = CustomerCard(
        application_id="TEST-001",
        phone="+996000000000"
    )

    # Initial CustomerCard stage
    assert customer.stage == "new"

    transition_stage(
        customer,
        ApplicationStage.COLLECTING_INFORMATION
    )
    assert customer.stage == "collecting_information"

    transition_stage(
        customer,
        ApplicationStage.PROCESSING_APPLICATION
    )
    assert customer.stage == "processing_application"

    transition_stage(
        customer,
        ApplicationStage.BUSINESS_DECISION
    )
    assert customer.stage == "business_decision"

    transition_stage(
        customer,
        ApplicationStage.COMPLETED
    )
    assert customer.stage == "completed"


def test_transition_after_decision():

    customer = CustomerCard(
        application_id="TEST-002",
        phone="+996000000001"
    )

    transition_after_decision(
        customer,
        "approved"
    )
    assert customer.stage == "approved"

    transition_after_decision(
        customer,
        "rejected"
    )
    assert customer.stage == "rejected"

    transition_after_decision(
        customer,
        "manual_review"
    )
    assert customer.stage == "manual_review"

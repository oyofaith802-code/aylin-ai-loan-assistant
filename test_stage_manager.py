from customer_card import CustomerCard
from stages import ApplicationStage
from stage_manager import set_stage


customer = CustomerCard(
    application_id="APP-001",
    phone="test_phone"
)

print("Before:", customer.current_stage)

set_stage(customer, ApplicationStage.COLLECTING_INFORMATION)

print("After:", customer.current_stage)
from customer_card import CustomerCard
from stages import ApplicationStage
from application_state import (
    transition_stage,
    get_current_stage
)


customer = CustomerCard(
    application_id="TEST-001",
    phone="+996000000000"
)


print("=" * 60)
print("APPLICATION STATE TEST")
print("=" * 60)


print("Initial stage:")
print(get_current_stage(customer))


transition_stage(
    customer,
    ApplicationStage.COLLECTING_INFORMATION
)

print("\nAfter information collection starts:")
print(get_current_stage(customer))


transition_stage(
    customer,
    ApplicationStage.PROCESSING_APPLICATION
)

print("\nAfter application processing starts:")
print(get_current_stage(customer))


transition_stage(
    customer,
    ApplicationStage.BUSINESS_DECISION
)

print("\nAfter business evaluation:")
print(get_current_stage(customer))


transition_stage(
    customer,
    ApplicationStage.COMPLETED
)

print("\nFinal stage:")
print(get_current_stage(customer))
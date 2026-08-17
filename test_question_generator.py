from customer_card import CustomerCard
from question_generator import generate_next_question


customer = CustomerCard(
    application_id="APP-001",
    phone="test_phone",
    car_model="Camry",
    car_year=2021,
    car_value=1500000,
    loan_amount=500000,
    loan_program="Автозалог",
    registration_region="Бишкек"
)

question = generate_next_question(customer)

print("Aylin's next question:")
print(question)
from question_generator import generate_question


fields = [
    "car_model",
    "car_year",
    "car_value",
    "loan_amount",
    "loan_program",
    "registration_region"
]


for field in fields:
    print(f"{field}:")
    print(generate_question(field))
    print()
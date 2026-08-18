QUESTIONS_RU = {

    "car_model":
        "Подскажите, пожалуйста, модель автомобиля?",

    "car_year":
        "Какого года ваш автомобиль?",

    "car_value":
        "Какова примерная стоимость автомобиля?",

    "loan_amount":
        "Какую сумму займа вы хотите получить?",

    "loan_program":
        "Какую программу займа вы рассматриваете?",

    "vehicle_possession":
        "Вы готовы передать автомобиль в залог или хотите оформить займ без передачи автомобиля?",

    "registration_region":
        "В каком регионе вы зарегистрированы?",

    "loan_term_months":
        "На какой срок вы хотите оформить займ?",
}


def generate_question(
    field: str
) -> str | None:

    return QUESTIONS_RU.get(field)
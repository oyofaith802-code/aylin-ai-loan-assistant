from customer_card import CustomerCard
from next_question import get_next_required_information
from question_generator import (
    generate_question,
    detect_language,
)


def process_information_stage(
    customer: CustomerCard,
    customer_message: str | None = None,
):

    next_field = get_next_required_information(
        customer
    )

    # --------------------------------------------------------
    # Complete
    # --------------------------------------------------------

    if next_field is None:

        return {
            "status": "information_complete",
            "question": None,
            "next_field": None,
        }

    # --------------------------------------------------------
    # Detect customer language
    # --------------------------------------------------------

    language = detect_language(
        customer_message or ""
    )

    # --------------------------------------------------------
    # Ask next question in customer's language
    # --------------------------------------------------------

    question = generate_question(
        next_field,
        language,
    )

    return {
        "status": "waiting_for_customer",
        "question": question,
        "next_field": next_field,
        "language": language,
    }

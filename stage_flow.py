from customer_card import CustomerCard
from next_question import get_next_required_information
from question_generator import generate_question


def process_information_stage(
    customer: CustomerCard
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
    # Ask next question
    # --------------------------------------------------------

    question = generate_question(
        next_field
    )

    return {
        "status": "waiting_for_customer",
        "question": question,
        "next_field": next_field,
    }
    
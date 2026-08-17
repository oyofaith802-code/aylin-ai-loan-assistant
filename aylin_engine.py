from customer_card import CustomerCard
from ai_card_updater import process_message_with_ai
from stage_manager import process_stage
from required_information import get_missing_information


def customer_card_to_dict(customer: CustomerCard) -> dict:
    """
    Convert CustomerCard into a dictionary.
    """

    return {
        "car_model": customer.car_model,
        "car_year": customer.car_year,
        "car_value": customer.car_value,
        "loan_amount": customer.loan_amount,
        "loan_program": customer.loan_program,
        "registration_region": customer.registration_region,
    }


def process_customer_message(
    customer: CustomerCard,
    message: str,
    conversation_history: list | None = None
) -> dict:
    """
    Main Aylin conversation engine.

    AI is used for information extraction.

    Deterministic logic controls:
    - customer data
    - required information
    - questions
    - application stage
    """

    conversation_history = conversation_history or []

    # ---------------------------------------------------------
    # 1. Extract information from customer message
    # ---------------------------------------------------------

    extracted_information = process_message_with_ai(
        customer,
        message
    )

    # ---------------------------------------------------------
    # 2. Process current application stage
    # ---------------------------------------------------------

    stage_result = process_stage(customer)

    # ---------------------------------------------------------
    # 3. Still collecting information
    # ---------------------------------------------------------

    if stage_result["status"] == "waiting_for_customer":

        missing_information = get_missing_information(
            customer
        )

        if missing_information:
            next_field = missing_information[0]
        else:
            next_field = None

        # -----------------------------------------------------
        # IMPORTANT
        #
        # Use the deterministic question directly.
        #
        # Do NOT send it through Ollama.
        # This prevents words such as "примерная"
        # from being corrupted.
        # -----------------------------------------------------

        question = stage_result["question"]

        return {
            "status": "waiting_for_customer",
            "response": question,
            "next_field": next_field,
            "stage": customer.stage,
            "extracted_information": extracted_information
        }

    # ---------------------------------------------------------
    # 4. Information collection completed
    # ---------------------------------------------------------

    if stage_result["status"] == "stage_completed":

        return {
            "status": "stage_completed",
            "response": "Спасибо. Вся необходимая информация получена.",
            "next_field": None,
            "stage": customer.stage,
            "extracted_information": extracted_information
        }

    # ---------------------------------------------------------
    # 5. Fallback
    # ---------------------------------------------------------

    return {
        "status": stage_result.get("status"),
        "response": stage_result.get("question"),
        "next_field": None,
        "stage": customer.stage,
        "extracted_information": extracted_information
    }
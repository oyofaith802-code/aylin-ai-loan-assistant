from customer_card import CustomerCard
from ai_card_updater import process_message_with_ai
from conversation_engine import process_customer_message


def process_ai_message(
    customer: CustomerCard,
    message: str
) -> dict:
    """
    Process a customer message using the AI extractor,
    update the customer card, then continue the business flow.
    """

    extracted_information = process_message_with_ai(
        customer,
        message
    )

    conversation = process_customer_message(
        customer,
        message
    )

    return {
        "extracted_information": extracted_information,
        "conversation": conversation,
        "customer_card": customer
    }
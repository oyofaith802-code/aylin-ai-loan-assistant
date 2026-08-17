from customer_card import CustomerCard
from message_extractor import extract_customer_information
from card_updater import update_customer_card
from conversation_engine import process_customer_message


def process_message(
    customer: CustomerCard,
    message: str
):
    """
    Process one customer message.

    1. Extract information
    2. Update customer card
    3. Continue the conversation
    """

    information = extract_customer_information(message)

    if information:
        update_customer_card(customer, information)

    result = process_customer_message(
        customer,
        message
    )

    return {
        "extracted_information": information,
        "customer_card": customer,
        "conversation": result
    }
from customer_card import CustomerCard
from required_information import get_missing_information


def get_next_required_information(
    customer: CustomerCard
) -> str | None:
    """
    Return the first missing required information field.

    The order here determines what Aylin asks for first.
    """

    missing = get_missing_information(customer)

    if not missing:
        return None

    return missing[0]
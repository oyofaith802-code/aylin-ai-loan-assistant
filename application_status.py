from application_repository import (
    get_application_by_phone,
    get_applications_by_phone
)


def get_application_status(phone: str) -> dict:
    """
    Return the latest application status for a customer.
    """

    application = get_application_by_phone(phone)

    if application is None:
        return {
            "found": False,
            "status": "not_found",
            "message": (
                "У вас пока нет зарегистрированной заявки."
            )
        }

    return {
        "found": True,
        "application_id": application.application_id,
        "stage": application.stage,
        "decision": application.decision,
        "decision_reason": application.decision_reason
    }


def get_application_history(phone: str) -> list:
    """
    Return all applications belonging to a customer.
    """

    applications = get_applications_by_phone(phone)

    result = []

    for application in applications:

        result.append({
            "application_id": application.application_id,
            "car_model": application.car_model,
            "car_year": application.car_year,
            "loan_amount": application.loan_amount,
            "stage": application.stage,
            "decision": application.decision,
            "decision_reason": application.decision_reason
        })

    return result
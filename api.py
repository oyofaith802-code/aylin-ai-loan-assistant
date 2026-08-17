from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field


from persistent_conversation import (
    process_persistent_message
)

from application_manager import (
    get_current_application,
    get_customer_application_history,
    start_new_application
)


router = APIRouter()


# =========================================================
# MODELS
# =========================================================


class ConversationRequest(BaseModel):

    phone: str = Field(...)

    message: str = Field(...)

    application_id: str | None = None



class NewApplicationRequest(BaseModel):

    phone: str



# =========================================================
# HELPERS
# =========================================================


def clean(value):

    return str(value).strip()



def customer_response(customer):

    if not customer:

        return None


    return {

        "application_id":
            customer.application_id,

        "phone":
            customer.phone,

        "car_model":
            customer.car_model,

        "car_year":
            customer.car_year,

        "car_value":
            customer.car_value,

        "loan_amount":
            customer.loan_amount,

        "loan_program":
            customer.loan_program,

        "loan_term_months":
            customer.loan_term_months,

        "vehicle_possession":
            customer.vehicle_possession,

        "registration_region":
            customer.registration_region,

        "stage":
            customer.stage,

        "decision":
            customer.decision,

    }



# =========================================================
# CHAT API
# =========================================================


@router.post("/conversation/message")
def conversation(
    request: ConversationRequest
):

    phone = clean(
        request.phone
    )


    message = clean(
        request.message
    )


    result = process_persistent_message(
        phone=phone,
        message=message,
        application_id=request.application_id
    )


    customer = result.get(
        "customer"
    )


    return {


        "application_id":
            (
                customer.application_id
                if customer
                else None
            ),


        "status":
            result.get("status"),


        "response":
            result.get("response"),


        "stage":
            result.get("stage"),


        "next_field":
            result.get("next_field"),


        "decision":
            result.get("decision"),


        "customer":
            customer_response(customer)

    }



# =========================================================
# NEW APPLICATION
# =========================================================


@router.post("/applications/new")
def create_application(
    request: NewApplicationRequest
):

    customer = start_new_application(
        request.phone
    )


    return {


        "application_id":
            customer.application_id,


        "phone":
            customer.phone,


        "stage":
            customer.stage

    }



# =========================================================
# CURRENT APPLICATION
# =========================================================


@router.get(
    "/applications/current/{phone}"
)
def current_application(
    phone:str
):

    customer = get_current_application(
        phone
    )


    if not customer:

        raise HTTPException(
            404,
            "Application not found"
        )


    return customer_response(
        customer
    )



# =========================================================
# HISTORY
# =========================================================


@router.get(
    "/applications/history/{phone}"
)
def history(
    phone:str
):

    return {


        "phone":
            phone,


        "applications":
            get_customer_application_history(
                phone
            )

    }
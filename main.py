from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from persistent_conversation import (
    process_persistent_message
)

from application_manager import (
    get_current_application,
    get_customer_application_history,
    start_new_application,
)

from application_repository import (
    get_conversation_history,
)

from wazzup_api import router as wazzup_router
from dashboard_api import router as dashboard_router


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Aylin AI Loan Assistant",
    description="AI-powered loan application assistant",
    version="1.2.0",
)


# ============================================================
# INCLUDE WAZZUP ROUTES
# ============================================================

app.include_router(
    wazzup_router
)

app.include_router(
    dashboard_router
)


# ============================================================
# PERSISTENT CONVERSATION HISTORY
# ============================================================

@app.get(
    "/applications/conversation/{application_id}"
)
def conversation_history(
    application_id: str
):

    messages = get_conversation_history(
        application_id
    )

    return {
        "application_id": application_id,
        "messages": [
            {
                "id": message.id,
                "sender": message.sender,
                "message": message.message,
                "created_at": (
                    message.created_at.isoformat()
                    if message.created_at
                    else None
                ),
            }
            for message in messages
        ],
    }


# ============================================================
# REQUEST MODELS
# ============================================================

class ConversationRequest(BaseModel):

    phone: str = Field(
        ...,
        min_length=1
    )

    message: str = Field(
        ...,
        min_length=1
    )

    application_id: str | None = None



class NewApplicationRequest(BaseModel):

    phone: str = Field(
        ...,
        min_length=1
    )


# ============================================================
# HELPERS
# ============================================================

def clean_phone(phone):

    return str(phone).strip()



def clean_message(message):

    return str(message).strip()



def customer_response(customer):

    if customer is None:
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

        "decision_reason":
            customer.decision_reason,
    }



# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {

        "service":
            "Aylin AI Loan Assistant",

        "status":
            "running",

        "version":
            "1.2.0"

    }



# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():

    return {

        "status":
            "healthy",

        "service":
            "aylin"

    }



# ============================================================
# DIRECT API CHAT TEST
# ============================================================

@app.post("/conversation/message")
def conversation(
    request: ConversationRequest
):

    phone = clean_phone(
        request.phone
    )

    message = clean_message(
        request.message
    )


    try:

        result = process_persistent_message(

            phone=phone,

            message=message,

            application_id=request.application_id

        )


    except Exception as e:

        print(
            "Conversation error:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail="Conversation processing failed"
        )


    customer = result.get(
        "customer"
    )


    return {

        "application_id":
            result.get(
                "application_id"
            ),

        "status":
            result.get(
                "status"
            ),

        "response":
            result.get(
                "response"
            ),

        "stage":
            result.get(
                "stage"
            ),

        "next_field":
            result.get(
                "next_field"
            ),

        "decision":
            result.get(
                "decision"
            ),

        "customer":

            customer_response(
                customer
            )

    }



# ============================================================
# START NEW APPLICATION
# ============================================================

@app.post("/applications/new")
def create_application(
    request: NewApplicationRequest
):

    customer = start_new_application(
        clean_phone(
            request.phone
        )
    )


    return {

        "application_id":
            customer.application_id,

        "phone":
            customer.phone,

        "stage":
            customer.stage,

        "status":
            "created"

    }



# ============================================================
# CURRENT APPLICATION
# ============================================================

@app.get(
    "/applications/current/{phone}"
)
def current_application(
    phone: str
):

    customer = get_current_application(
        clean_phone(phone)
    )


    if customer is None:

        raise HTTPException(
            status_code=404,
            detail="No application found"
        )


    return customer_response(
        customer
    )



# ============================================================
# APPLICATION HISTORY
# ============================================================

@app.get(
    "/applications/history/{phone}"
)
def history(
    phone: str
):

    applications = (
        get_customer_application_history(
            clean_phone(phone)
        )
    )


    return {

        "phone":
            phone,

        "count":
            len(applications),

        "applications":
            applications

    }



# ============================================================
# API INFO
# ============================================================

@app.get("/api/info")
def api_info():

    return {

        "service":
            "Aylin AI Loan Assistant",

        "version":
            "1.2.0",

        "routes":

            [

                "/conversation/message",

                "/webhook/wazzup",

                "/applications/new",

                "/applications/current/{phone}",

                "/applications/history/{phone}",

                "/docs"

            ]

    }
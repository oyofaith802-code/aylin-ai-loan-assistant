from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from application_repository import (
    get_conversation_history,
)


router = APIRouter()

DASHBOARD_FILE = (
    Path(__file__).resolve().parent
    / "dashboard"
    / "index.html"
)


# ============================================================
# DASHBOARD PAGE
# ============================================================

@router.get("/dashboard")
async def dashboard():

    return FileResponse(
        DASHBOARD_FILE,
        media_type="text/html"
    )


# ============================================================
# CONVERSATION HISTORY
# ============================================================

@router.get(
    "/dashboard/conversation/{application_id}"
)
async def conversation_history(
    application_id: str
):

    try:

        messages = get_conversation_history(
            application_id
        )

        return [
            {
                "id": message.id,
                "application_id":
                    message.application_id,
                "phone":
                    message.phone,
                "sender":
                    message.sender,
                "message":
                    message.message,
                "created_at":
                    message.created_at.isoformat()
            }

            for message in messages
        ]

    except Exception as e:

        print(
            "Dashboard history error:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to load conversation history"
        )

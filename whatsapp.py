from __future__ import annotations

import os
import requests
from dotenv import load_dotenv


load_dotenv()


# ============================================================
# WAZZUP CONFIGURATION
# ============================================================

WAZZUP_API_TOKEN = os.getenv(
    "WAZZUP_API_TOKEN",
    ""
)

WAZZUP_API_URL = os.getenv(
    "WAZZUP_API_URL",
    "https://api.wazzup24.com/v3/message"
)


# ============================================================
# CONFIG CHECK
# ============================================================

def wazzup_configured() -> bool:
    """
    Check if Wazzup token exists.
    """

    return bool(
        WAZZUP_API_TOKEN
    )


# ============================================================
# SEND MESSAGE TO WHATSAPP THROUGH WAZZUP
# ============================================================

def send_whatsapp_message(
    recipient_phone: str,
    message: str,
):

    if not WAZZUP_API_TOKEN:

        raise RuntimeError(
            "WAZZUP_API_TOKEN is missing"
        )


    if not recipient_phone:

        raise ValueError(
            "Recipient phone is required"
        )


    if not message:

        raise ValueError(
            "Message is required"
        )


    headers = {

        "Authorization":
            f"Bearer {WAZZUP_API_TOKEN}",

        "Content-Type":
            "application/json"

    }


    payload = {

        "channelId":
            os.getenv(
                "WAZZUP_CHANNEL_ID",
                ""
            ),

        "chatType":
            "whatsapp",

        "chatId":
            recipient_phone,

        "text":
            message

    }


    response = requests.post(

        WAZZUP_API_URL,

        headers=headers,

        json=payload,

        timeout=30

    )


    if not response.ok:

        raise RuntimeError(

            "Wazzup API error: "

            f"{response.status_code} "

            f"{response.text}"

        )


    return response.json()



# ============================================================
# TEST CONNECTION
# ============================================================

def test_wazzup_connection():

    if not wazzup_configured():

        return {

            "status":
                "not_configured"

        }


    return {

        "status":
            "configured"

    }
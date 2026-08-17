import os
import requests
from dotenv import load_dotenv


load_dotenv()


# ============================================================
# WAZZUP CONFIG
# ============================================================

WAZZUP_API_KEY = os.getenv(
    "WAZZUP_API_KEY"
)

WAZZUP_CHANNEL_ID = os.getenv(
    "WAZZUP_CHANNEL_ID"
)

WAZZUP_API_URL = os.getenv(
    "WAZZUP_API_URL",
    "https://api.wazzup24.com"
)


# ============================================================
# CONFIG CHECK
# ============================================================

def check_wazzup_config():

    missing = []

    if not WAZZUP_API_KEY:
        missing.append(
            "WAZZUP_API_KEY"
        )

    if not WAZZUP_CHANNEL_ID:
        missing.append(
            "WAZZUP_CHANNEL_ID"
        )

    if missing:

        raise Exception(
            "Missing Wazzup config: "
            + ", ".join(missing)
        )


# ============================================================
# SEND MESSAGE TO WHATSAPP
# ============================================================

def send_wazzup_message(
    phone: str,
    text: str
):

    check_wazzup_config()


    if not phone:

        raise ValueError(
            "Phone is required"
        )


    if not text:

        raise ValueError(
            "Message text is required"
        )


    # Wazzup send message endpoint

    url = (
        f"{WAZZUP_API_URL}/v3/message"
    )


    headers = {

        "Authorization":
            f"Bearer {WAZZUP_API_KEY}",

        "Content-Type":
            "application/json"

    }


    payload = {

        "channelId":
            WAZZUP_CHANNEL_ID,

        "chatType":
            "whatsapp",

        "chatId":
            phone,

        "text":
            text

    }


    print("\n========== WAZZUP SEND ==========")
    print("URL:", url)
    print("PHONE:", phone)
    print("TEXT:", text)
    print("=================================\n")


    response = requests.post(

        url,

        headers=headers,

        json=payload,

        timeout=30

    )


    print(
        "WAZZUP RESPONSE:",
        response.status_code,
        response.text
    )


    if not response.ok:

        raise Exception(
            f"Wazzup API error: {response.text}"
        )


    return response.json()
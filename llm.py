from __future__ import annotations

import os
import requests
from typing import Optional
from dotenv import load_dotenv


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# ROUTERAI CONFIGURATION
# ============================================================

ROUTERAI_URL = "https://routerai.ru/api/v1/chat/completions"

# IMPORTANT:
# RouterAI requires the provider/model format.
MODEL = "openai/gpt-4o-mini"


# ============================================================
# API KEY
# ============================================================

# Recommended:
# Set ROUTERAI_API_KEY as an environment variable.
#
# Windows CMD:
# set ROUTERAI_API_KEY=YOUR_ROUTERAI_KEY
#
# Do NOT commit the real API key to GitHub.

ROUTERAI_API_KEY = os.getenv("ROUTERAI_API_KEY")


# ============================================================
# AI REQUEST
# ============================================================

def ask_ai(
    prompt: str,
    model: Optional[str] = None,
) -> str:
    """
    Send a prompt to RouterAI and return the AI response.
    """

    if not ROUTERAI_API_KEY:

        raise RuntimeError(
            "ROUTERAI_API_KEY is not configured."
        )

    if not prompt or not prompt.strip():

        raise ValueError(
            "Prompt cannot be empty."
        )

    selected_model = (
        model
        or MODEL
    )

    headers = {
        "Authorization":
            f"Bearer {ROUTERAI_API_KEY}",

        "Content-Type":
            "application/json",
    }

    payload = {

        "model":
            selected_model,

        "messages": [

            {
                "role": "user",

                "content":
                    prompt.strip(),
            }
        ],

        "stream":
            False,
    }

    try:

        response = requests.post(

            ROUTERAI_URL,

            headers=headers,

            json=payload,

            timeout=120,
        )

    except requests.RequestException as error:

        raise RuntimeError(
            f"RouterAI connection error: {error}"
        ) from error


    # ========================================================
    # ERROR HANDLING
    # ========================================================

    if not response.ok:

        try:
            error_data = response.json()

        except ValueError:
            error_data = response.text

        raise RuntimeError(
            f"RouterAI API error "
            f"(HTTP {response.status_code}): "
            f"{error_data}"
        )


    # ========================================================
    # PARSE RESPONSE
    # ========================================================

    try:

        data = response.json()

    except ValueError as error:

        raise RuntimeError(
            "RouterAI returned invalid JSON."
        ) from error


    # ========================================================
    # EXTRACT MESSAGE
    # ========================================================

    try:

        content = (
            data["choices"][0]
            ["message"]
            ["content"]
        )

    except (
        KeyError,
        IndexError,
        TypeError,
    ) as error:

        raise RuntimeError(
            f"Unexpected RouterAI response: "
            f"{data}"
        ) from error


    if not isinstance(content, str):

        raise RuntimeError(
            f"RouterAI returned invalid content: "
            f"{content}"
        )

    return content.strip()


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("ROUTERAI TEST")
    print("=" * 60)

    try:

        response = ask_ai(
            "Ответь одним коротким предложением: "
            "что такое автозалог?"
        )

        print()
        print("MODEL:", MODEL)

        print()
        print("RESPONSE:")
        print(response)

        print()
        print("ROUTERAI TEST PASSED")

    except Exception as error:

        print()
        print("ROUTERAI TEST FAILED")

        print()
        print(error)
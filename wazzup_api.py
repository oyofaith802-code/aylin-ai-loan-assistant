from fastapi import APIRouter, Request

from wazzup_client import send_wazzup_message
from persistent_conversation import process_persistent_message
from audio_transcription import transcribe_audio_from_url


router = APIRouter()


@router.get("/webhook/wazzup")
async def wazzup_webhook_check():
    return {"status": "ok"}


@router.post("/webhook/wazzup")
async def wazzup_webhook(request: Request):

    data = await request.json()

    print("\n========== WAZZUP RECEIVED ==========")
    print(data)
    print("=====================================\n")

    if not data:
        return {"status": "ok"}

    messages = data.get("messages", [])

    if not messages:
        print("WAZZUP: No messages in webhook payload")
        return {"status": "ok"}

    for msg in messages:

        print("\n---------- WAZZUP MESSAGE ----------")
        print(msg)
        print("------------------------------------\n")

        if msg.get("isEcho") is True:
            print("WAZZUP: IGNORING ECHO MESSAGE")
            continue

        channel_id = msg.get("channelId")
        chat_id = msg.get("chatId")
        phone = chat_id

        message_type = msg.get("type")
        text = msg.get("text")
        content_uri = msg.get("contentUri")

        print("MESSAGE TYPE:", message_type)
        print("CHANNEL ID:", channel_id)
        print("CHAT ID:", chat_id)
        print("PHONE:", phone)

        # =====================================================
        # AUDIO
        # =====================================================

        if message_type == "audio":

            if not content_uri:
                print("WAZZUP: Audio message has no contentUri")
                continue

            print("\n========== AUDIO MESSAGE ==========")
            print("AUDIO URL:", content_uri)

            try:
                text = transcribe_audio_from_url(
                    content_uri
                )

                print(
                    "\n========== AUDIO TRANSCRIPTION =========="
                )
                print("TRANSCRIPTION:", text)
                print("==========================================\n")

            except Exception as error:

                print(
                    "WAZZUP AUDIO TRANSCRIPTION ERROR:",
                    error
                )

                continue

        # =====================================================
        # TEXT
        # =====================================================

        elif message_type in ("text", "chat"):

            if not text:
                print("WAZZUP: Text message has no text")
                continue

        # =====================================================
        # UNSUPPORTED MESSAGE
        # =====================================================

        else:

            print(
                "WAZZUP: Unsupported message type:",
                message_type
            )

            continue

        # =====================================================
        # VALIDATION
        # =====================================================

        if not text:
            print("WAZZUP: Message has no usable text")
            continue

        if not phone:
            print("WAZZUP: Could not determine customer phone")
            continue

        print("\n========== AYLIN INPUT ==========")
        print("PHONE:", phone)
        print("MESSAGE:", text)
        print("=================================\n")

        # =====================================================
        # AYLIN
        # =====================================================

        try:

            result = process_persistent_message(
                phone=phone,
                message=text,
                application_id=None
            )

            aylin_response = result.get("response")

            print(
                "\n========== AYLIN RESPONSE =========="
            )
            print(aylin_response)
            print("=====================================\n")

        except Exception as error:

            print(
                "AYLIN PROCESSING ERROR:",
                error
            )

            continue

        # =====================================================
        # SEND RESPONSE
        # =====================================================

        if aylin_response:

            try:

                send_wazzup_message(
                    phone=phone,
                    text=aylin_response
                )

                print(
                    "========== WAZZUP RESPONSE SENT =========="
                )

            except Exception as error:

                print(
                    "WAZZUP SEND ERROR:",
                    error
                )

    return {"status": "ok"}

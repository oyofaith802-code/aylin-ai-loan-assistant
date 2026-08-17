import os
import tempfile
import requests


WHISPER_MODEL = None


def transcribe_audio_from_url(url: str) -> str:

    global WHISPER_MODEL

    if not url:
        raise ValueError("Audio URL is missing")

    # Load Whisper only when an audio message is actually received.
    # This prevents Render from loading the model during API startup.
    if WHISPER_MODEL is None:

        import whisper

        print("Loading Whisper model...")

        WHISPER_MODEL = whisper.load_model("base")

        print("Whisper model loaded.")

    print("\n========== AUDIO TRANSCRIPTION ==========")
    print("AUDIO URL:", url)

    response = requests.get(
        url,
        timeout=60
    )

    response.raise_for_status()

    audio_data = response.content

    print(
        "AUDIO SIZE:",
        len(audio_data),
        "bytes"
    )

    with tempfile.NamedTemporaryFile(
        suffix=".mp3",
        delete=False
    ) as temp_file:

        temp_path = temp_file.name

        temp_file.write(audio_data)

    try:

        print("TRANSCRIBING AUDIO...")

        result = WHISPER_MODEL.transcribe(
            temp_path,
            language="ru",
            fp16=False
        )

        text = result.get(
            "text",
            ""
        ).strip()

        print("TRANSCRIPTION:", text)
        print("=========================================\n")

        return text

    finally:

        try:
            os.remove(temp_path)
        except OSError:
            pass

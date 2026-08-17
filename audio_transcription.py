import os
import tempfile
import requests
import whisper


print("Loading Whisper model...")
WHISPER_MODEL = whisper.load_model("base")
print("Whisper model loaded.")


def transcribe_audio_from_url(url: str) -> str:

    if not url:
        raise ValueError("Audio URL is missing")

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

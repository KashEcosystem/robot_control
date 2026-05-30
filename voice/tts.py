import subprocess
from gtts import gTTS
from core.logger_config import logger


TTS_ENGINE = "gtts"
OUTPUT_FILE = "/tmp/robot_voice.mp3"
SPEAKER_TARGET = "91"


def speak(text: str) -> None:
    if not text:
        return

    print(f"ROBOT SPEAK: {text}")
    logger.info(f"[TTS] speak={text}")

    try:
        if TTS_ENGINE == "gtts":
            tts = gTTS(text=text, lang="vi")
            tts.save(OUTPUT_FILE)

            subprocess.run(
                ["pw-play", "--target", SPEAKER_TARGET, OUTPUT_FILE],
                check=False
            )

        else:
            subprocess.run(
                ["espeak-ng", "-v", "vi", "-s", "140", text],
                check=False
            )

    except Exception:
        logger.exception("[TTS] speak failed")
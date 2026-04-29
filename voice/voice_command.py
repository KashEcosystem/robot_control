from core.logger_config import logger
from voice.voice_state import VoiceState

def parse_voice_command(text: str) -> VoiceState:
    voice = VoiceState(text=text)

    if not text:
        voice.command = "none"
        voice.active = False
        return voice

    if "stop" in text or "dừng" in text:
        voice.command = "stop"
        voice.confidence = 1.0
        voice.active = True

    elif "forward" in text or "tiến" in text:
        voice.command = "forward"
        voice.confidence = 1.0
        voice.active = True

    elif "back" in text or "lùi" in text:
        voice.command = "backward"
        voice.confidence = 1.0
        voice.active = True

    elif "left" in text or "trái" in text:
        voice.command = "left"
        voice.confidence = 1.0
        voice.active = True

    elif "right" in text or "phải" in text:
        voice.command = "right"
        voice.confidence = 1.0
        voice.active = True

    elif "scan" in text or "quét" in text:
        voice.command = "scan"
        voice.confidence = 1.0
        voice.active = True

    else:
        voice.command = "unknown"
        voice.confidence = 0.3
        voice.active = False

    logger.info(
        f"[VOICE] parsed text={voice.text} command={voice.command} active={voice.active}"
    )

    return voice
from core.logger_config import logger

def get_voice_text() -> str:
    """
    Mock voice input.
    Sau này sẽ thay bằng mic thật + speech-to-text.
    """
    try:
        text = input("Say command > ").strip().lower()
        logger.info(f"[VOICE] input text={text}")
        return text
    except Exception:
        logger.exception("[VOICE] get_voice_text failed")
        return ""
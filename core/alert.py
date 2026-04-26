import time
import requests

from core.config import settings
from core.logger_config import logger

_last_alert_time = {}
ALERT_COOLDOWN_SECONDS = 60

def send_alert(message: str, level: str = "ERROR", key: str | None=None):
    if not settings.TELEGRAM_ENABLED:
         
           logger.info(f"[ALERT_DISABLED] {level}: {message}")
           print(f"[ALERT_DISABLED] {level}: {message}")
           return
    
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        logger.warning("[ALERT] Telegram config missing")
        return
    
    alert_key = key or message
    now = time.time()

    last_time = _last_alert_time.get(alert_key, 0)
    if now - last_time < ALERT_COOLDOWN_SECONDS:
        return
    
    _last_alert_time[alert_key] = now

    text = (f"[{level}] {settings.ROBOT_NAME}\n"
            f"{message}")
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    
    payload = {"chat_id": settings.TELEGRAM_CHAT_ID,
               "text": text }
    
    try:
        requests.post(url, json = payload, timeout = 5)
    except Exception:
        logger.exception("[ALERT] Failed to send telegram alert")
from picamera2 import Picamera2
from core.logger_config import logger

picam2 = None

def init_camera():
    global picam2
    try:
        picam2 = Picamera2()
        picam2.start()
        logger.info("[CAMERA] initialized (picamera2)")
    except Exception:
        logger.exception("[CAMERA] init failed")

def get_frame():
    try:
        if picam2 is None:
            logger.warning("[CAMERA] picam2 is None")
            return None

        frame = picam2.capture_array()
        return frame

    except Exception:
        logger.exception("[CAMERA] get_frame failed")
        return None

def cleanup():
    global picam2
    logger.info("[CAMERA] cleanup start")
    if picam2:
        picam2.stop()
    logger.info("[CAMERA] cleanup done")
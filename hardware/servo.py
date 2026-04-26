from adafruit_servokit import ServoKit

from core.config import (
    PAN_MIN,
    PAN_MAX,
    TILT_MIN,
    TILT_MAX,
    PAN_DEFAULT,
    TILT_DEFAULT,
)
from core.logger_config import logger


kit = ServoKit(channels=16)

PAN_CHANNEL = 1
TILT_CHANNEL = 2


def clamp_angle(angle: int, min_angle: int, max_angle: int) -> int:
    return max(min_angle, min(max_angle, angle))


def set_pan(angle: int) -> int:
    try:
        angle = clamp_angle(angle, PAN_MIN, PAN_MAX)
        kit.servo[PAN_CHANNEL].angle = angle
        logger.info(f"[SERVO] pan={angle}")
        return angle

    except Exception:
        logger.exception(f"[SERVO] set_pan failed angle={angle}")
        return clamp_angle(angle, PAN_MIN, PAN_MAX)


def set_tilt(angle: int) -> int:
    try:
        angle = clamp_angle(angle, TILT_MIN, TILT_MAX)
        kit.servo[TILT_CHANNEL].angle = angle
        logger.info(f"[SERVO] tilt={angle}")
        return angle

    except Exception:
        logger.exception(f"[SERVO] set_tilt failed angle={angle}")
        return clamp_angle(angle, TILT_MIN, TILT_MAX)


def set_angles(pan_angle: int, tilt_angle: int) -> tuple[int, int]:
    pan_angle = set_pan(pan_angle)
    tilt_angle = set_tilt(tilt_angle)
    return pan_angle, tilt_angle


def center_camera() -> tuple[int, int]:
    logger.info("[SERVO] center_camera")
    return set_angles(PAN_DEFAULT, TILT_DEFAULT)


def cleanup() -> None:
    logger.info("[SERVO] cleanup start")

    try:
        center_camera()
        logger.info("[SERVO] cleanup done")

    except Exception:
        logger.exception("[SERVO] cleanup failed")
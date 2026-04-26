import RPi.GPIO as GPIO

from core.logger_config import logger


IN1 = 13
IN2 = 12
IN3 = 21
IN4 = 20
ENA = 6
ENB = 26
PWM_FREQ = 100


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)

pwm_left = GPIO.PWM(ENA, PWM_FREQ)
pwm_right = GPIO.PWM(ENB, PWM_FREQ)

pwm_left.start(20)
pwm_right.start(20)


def _clamp_speed(speed: int) -> int:
    return max(0, min(100, speed))


def _set_left_motor(forward: bool, speed: int) -> None:
    speed = _clamp_speed(speed)

    try:
        if forward:
            GPIO.output(IN1, 1)
            GPIO.output(IN2, 0)
        else:
            GPIO.output(IN1, 0)
            GPIO.output(IN2, 1)

        pwm_left.ChangeDutyCycle(speed)

    except Exception:
        logger.exception(f"[MOTOR] left failed forward={forward} speed={speed}")


def _set_right_motor(forward: bool, speed: int) -> None:
    speed = _clamp_speed(speed)

    try:
        if forward:
            GPIO.output(IN3, 1)
            GPIO.output(IN4, 0)
        else:
            GPIO.output(IN3, 0)
            GPIO.output(IN4, 1)

        pwm_right.ChangeDutyCycle(speed)

    except Exception:
        logger.exception(f"[MOTOR] right failed forward={forward} speed={speed}")


def forward(speed: int = 50) -> None:
    speed = _clamp_speed(speed)
    _set_left_motor(forward=True, speed=speed)
    _set_right_motor(forward=True, speed=speed)


def backward(speed: int = 50) -> None:
    speed = _clamp_speed(speed)
    _set_left_motor(forward=False, speed=speed)
    _set_right_motor(forward=False, speed=speed)


def left(speed: int = 50) -> None:
    speed = _clamp_speed(speed)
    _set_left_motor(forward=False, speed=speed)
    _set_right_motor(forward=True, speed=speed)


def right(speed: int = 50) -> None:
    speed = _clamp_speed(speed)
    _set_left_motor(forward=True, speed=speed)
    _set_right_motor(forward=False, speed=speed)


def stop() -> None:
    try:
        pwm_left.ChangeDutyCycle(0)
        pwm_right.ChangeDutyCycle(0)

        GPIO.output(IN1, 0)
        GPIO.output(IN2, 0)
        GPIO.output(IN3, 0)
        GPIO.output(IN4, 0)

        logger.info("[MOTOR] stop")

    except Exception:
        logger.exception("[MOTOR] stop failed")


def apply_motor_command(command: str, speed: int = 30) -> None:
    speed = _clamp_speed(speed)

    logger.info(f"[MOTOR] command={command} speed={speed}")

    if command == "forward":
        forward(speed)

    elif command == "backward":
        backward(speed)

    elif command == "left":
        left(speed)

    elif command == "right":
        right(speed)

    elif command == "stop":
        stop()

    else:
        logger.warning(f"[MOTOR] unknown command={command} -> stop")
        stop()


def cleanup() -> None:
    logger.info("[MOTOR] cleanup start")

    try:
        stop()
        pwm_left.stop()
        pwm_right.stop()
        GPIO.cleanup()
        logger.info("[MOTOR] cleanup done")

    except Exception:
        logger.exception("[MOTOR] cleanup failed")

    
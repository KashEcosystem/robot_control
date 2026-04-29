from core.logger_config import logger
from core.config import (
    PAN_MIN,
    PAN_MAX,
    TILT_MIN,
    SCAN_DIRECTION,
    SCAN_PAN_STEP,
    SCAN_TILT_STEP,
    SCAN_MOVE_SPEED,
    TILT_DEFAULT
)


def _move_tilt_step(state) -> None:
    state.tilt_angle += SCAN_TILT_STEP

    if state.tilt_angle > TILT_MIN:
        state.tilt_angle = TILT_MIN


def scan_step(state) -> None:
    try:
        if state.obstacle_detected:
            state.move_command = "stop"
            state.move_speed = 0
            state.action_reason = "scan_stop_obstacle"
        else:
            state.move_command = "forward"
            state.move_speed = SCAN_MOVE_SPEED
            state.action_reason = "scan_crawl_search"

        state.pan_angle += state.scan_direction * SCAN_PAN_STEP

        if state.pan_angle >= PAN_MAX:
            state.pan_angle = PAN_MAX
            state.scan_direction = -SCAN_DIRECTION

        elif state.pan_angle <= PAN_MIN:
            state.pan_angle = PAN_MIN
            state.scan_direction = SCAN_DIRECTION
        state.tilt_angle = TILT_DEFAULT

        logger.info(
            f"[SCAN] pan={state.pan_angle} "
            f"tilt={state.tilt_angle} "
            f"direction={state.scan_direction} "
            f"cmd={state.move_command} "
            f"speed={state.move_speed} "
            f"reason={state.action_reason}"
        )

    except Exception:
        logger.exception("[SCAN] scan_step failed")
        state.error_message = "scanner failed"
        state.move_command = "stop"
        state.move_speed = 0
        state.action_reason = "scan_error"
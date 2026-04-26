from core.logger_config import logger
from core.config import(PAN_MIN, PAN_MAX, TILT_MIN, TILT_MAX, SCAN_PAN_STEP, SCAN_TILT_STEP, SCAN_DIRECTION)


def _move_tilt_step(state) -> None:
    state.tilt_angle += SCAN_TILT_STEP

    if state.tilt_angle > TILT_MAX:
        state.tilt_angle = TILT_MIN

def scan_step(state) -> None:
    try:
        state.move_command = "stop"
        state.move_speed = 0
        state.pan_angle += state.scan_direction * SCAN_PAN_STEP

        if state.pan_angle >= PAN_MAX:
            state.pan_angle = PAN_MAX
            state.scan_direction = SCAN_DIRECTION
            _move_tilt_step(state)
        elif state.pan_angle <= PAN_MIN:
            state.pan_angle = PAN_MIN
            state.scan_direction = SCAN_DIRECTION
            _move_tilt_step(state)
        logger.info(f'[SCAN] pan={state.pan_angle} tilt={state.tilt_angle} direction={state.scan_direction}')
    except Exception:
        logger.exception(f"[SCAN] scan_step failed")
        state.error_message = "scanner failed"
        state.move_command = "stop"
        state.move_speed = 0
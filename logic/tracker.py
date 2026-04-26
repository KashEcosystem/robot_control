from core.logger_config import logger
from core.config import (
    MOVE_TOLERANCE_X,
    LOW_SPEED,
    HIGH_SPEED,
    MEDIUM_SPEED,
    TARGET_AREA_FAR,
    TARGET_AREA_MEDIUM,
    TARGET_AREA_NEAR,
)


def tracking_step(state):
    try:
        center_x = state.frame_width // 2
        center_y = state.frame_height // 2

        error_x = state.target_x - center_x
        error_y = state.target_y - center_y

        state.offset_x = error_x
        state.offset_y = error_y

        if abs(error_x) > 10:
           state.pan_angle += int(error_x * 0.01)

        if abs(error_y) > 10:
           state.tilt_angle -= int(error_y * 0.01)

        state.pan_angle = max(0, min(180, state.pan_angle))
        state.tilt_angle = max(0, min(180, state.tilt_angle))

        # ====== TURN LEFT / RIGHT ======
        if abs(error_x) > 20:
            if error_x > 0:
                state.move_command = "right"
            else:
                state.move_command = "left"

            target_speed = min(int(abs(error_x)*0.4), 100)
            state.move_speed = int(state.prev_speed * 0.7 + target_speed * 0.3)
            state.prev_speed = state.move_speed

        # ====== FORWARD / STOP ======
        else:
            if state.target_area < TARGET_AREA_FAR:
                state.move_command = "forward"
                state.move_speed = HIGH_SPEED

            elif state.target_area < TARGET_AREA_MEDIUM:
                state.move_command = "forward"
                state.move_speed = MEDIUM_SPEED

            elif state.target_area < TARGET_AREA_NEAR:
                state.move_command = "forward"
                state.move_speed = LOW_SPEED

            else:
                state.move_command = "stop"
                state.move_speed = 0

        logger.info(
            f"[TRACK] x={state.target_x} y={state.target_y} "
            f"error_x={error_x} error_y={error_y} "
            f"area={state.target_area} "
            f"cmd={state.move_command} speed={state.move_speed}"
        )

    except Exception:
        logger.exception("[TRACK] tracking_step failed")
        state.move_command = "stop"
        state.move_speed = 0
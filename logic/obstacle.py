from core.logger_config import logger
from core.config import (
    OBSTACLE_DISTANCE_CM,
    DANGER_DISTANCE_CM,
    AVOID_SPEED,
    DANGER_SPEED,
)


def update_obstacle_state(state):
    if state.distance_cm <= DANGER_DISTANCE_CM:
        state.obstacle_detected = True
        state.obstacle_level = "danger"

    elif state.distance_cm <= OBSTACLE_DISTANCE_CM:
        state.obstacle_detected = True
        state.obstacle_level = "warning"

    else:
        state.obstacle_detected = False
        state.obstacle_level = "clear"


def avoid_obstacle_step(state):
    if state.distance_cm <= DANGER_DISTANCE_CM:
        state.move_command = "backward"
        state.move_speed = DANGER_SPEED
        state.action_reason = "danger_backward"

        logger.warning(
            f"[OBSTACLE] danger distance={state.distance_cm} "
            f"cmd={state.move_command} speed={state.move_speed}"
        )
        return

    # né ngược hướng đang scan
    if state.scan_direction == 1:
        state.move_command = "left"
        state.action_reason = "avoid_left_from_scan_right"
    else:
        state.move_command = "right"
        state.action_reason = "avoid_right_from_scan_left"

    state.move_speed = AVOID_SPEED

    logger.info(
        f"[OBSTACLE] avoid distance={state.distance_cm} "
        f"level={state.obstacle_level} "
        f"cmd={state.move_command} "
        f"speed={state.move_speed} "
        f"reason={state.action_reason}"
    )
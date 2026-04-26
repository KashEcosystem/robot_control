from core.logger_config import logger

OBSTACLE_DISTANCE_CM = 20
DANGER_DISTANCE_CM = 10
AVOID_SPEED = 25
DANGER_SPEED = 15


def update_obstacle_state(state):

    if state.distance_cm <= OBSTACLE_DISTANCE_CM:
        state.obstacle_detected = True
    else:
        state.obstacle_detected = False


def avoid_obstacle_step(state):

    if state.distance_cm <= DANGER_DISTANCE_CM:
        state.move_command = "backward"
        state.move_speed = DANGER_SPEED

        logger.warning(f"[OBSTACLE] danger distance={state.distance_cm}"
                       f"cmd={state.move_command} speed={state.move_speed}")
        return
    
    if state.scan_direction == 1:
        state.move_command = "left"
    else:
        state.move_command = "right"

    state.move_speed = AVOID_SPEED

    logger.info(f"[OBSTACLE] avoid distance={state.distance_cm}"
                f"cmd={state.move_command} speed={state.move_speed}")
import cv2
from hardware.camera import get_frame
from logic.detector import detect_target
from logic.memory import update_memory
from logic.decision import decide_mode
from logic.tracker import tracking_step
from logic.scanner import scan_step
from logic.obstacle import update_obstacle_state, avoid_obstacle_step
from logic.visualize import draw_debug
from logic.execute import apply_output

from core.logger_config import logger


def tracking_memory_step(state):
    if state.last_direction == "right":
        state.move_command = "right"
    elif state.last_direction == "left":
        state.move_command = "left"
    else:
        state.move_command = "forward"

    state.move_speed = 20


def error_step(state):
    state.move_command = "stop"
    state.move_speed = 0


MODE_HANDLERS = {
    "tracking": tracking_step,
    "tracking_memory": tracking_memory_step,
    "scan": scan_step,
    "avoid_obstacle": avoid_obstacle_step,
    "error": error_step,
}


def run_step(state):
    frame = get_frame()
    state.frame = frame

    if frame is None:
        state.camera_fail_count += 1
        state.error_message = "camera frame is None"
        state.target_detected = False
    else:
        state.camera_fail_count = 0
        state.error_message = None
        state.frame_height, state.frame_width = frame.shape[:2]
        detect_target(state)

    update_memory(state)

    # Level 3: cập nhật trạng thái vật cản
    update_obstacle_state(state)

    new_mode = decide_mode(state)

    if new_mode != state.mode:
        logger.info(f"[STATE] {state.mode} -> {new_mode}")

    state.mode = new_mode

    handler = MODE_HANDLERS.get(state.mode, error_step)
    handler(state)

    debug_frame = draw_debug(state)
    if debug_frame is not None:
        cv2.imwrite("debug.jpg", debug_frame)

    apply_output(state)

    logger.info(
        f"[RUN] mode={state.mode} "
        f"target={state.target_detected} "
        f"lost={state.lost_count} "
        f"obstacle={state.obstacle_detected} "
        f"distance={state.distance_cm} "
        f"cmd={state.move_command} "
        f"speed={state.move_speed} "
        f"pan={state.pan_angle} "
        f"tilt={state.tilt_angle}"
    )
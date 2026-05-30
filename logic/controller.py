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
from core.alert import send_alert
from core.trace import RobotTrace
from voice.voice_service import VoiceService

from core.logger_config import logger

voice_service = VoiceService()


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

def manual_step(state):
    state.move_command = state.voice_command
    state.move_speed = 25

def idle_step(state):
    state.move_command = "stop"
    state.move_speed = 0


MODE_HANDLERS = {
    "tracking": tracking_step,
    "tracking_memory": tracking_memory_step,
    "scan": scan_step,
    "avoid_obstacle": avoid_obstacle_step,
    "manual": manual_step,
    "idle": idle_step,
    "error": error_step,
}


def run_step(state):
    frame = get_frame()
    state.frame = frame
    trace = RobotTrace(state)
    trace.step( "camera start")

    if frame is None:
        state.camera_fail_count += 1
        state.error_message = "camera frame is None"
        state.target_detected = False

        if state.camera_fail_count == 1:
            send_alert("Camera failed: frame is None",
                       level = "ERROR",
                       key = "camera_fail")
    else:
        state.camera_fail_count = 0
        state.error_message = None
        state.frame_height, state.frame_width = frame.shape[:2]
        trace.step("detect start")
        detect_target(state)
        trace.step("detect done", f"target={state.target_detected}")

    trace.step("memory start")
    update_memory(state)
    trace.step("memory done", f"lost={state.lost_count}")

    # Level 3: cập nhật trạng thái vật cản
    trace.step("obstacle start")
    update_obstacle_state(state)
    trace.step("obstacle done", f"obstacle={state.obstacle_detected}")

    trace.step("voice start")
    voice_state = voice_service.listen_and_process()
    state.voice_active = voice_state.active
    state.voice_text = voice_state.text
    state.voice_command = voice_state.command
    state.voice_confidence = voice_state.confidence
    trace.step("voice done", f"active={state.voice_active} command={state.voice_command}")

    trace.step("decision start")
    old_mode = state.mode
    new_mode = decide_mode(state)
    state.mode = new_mode
    trace.step("decision done", f"mode={new_mode} reason={state.decision_reason}")


    if old_mode != state.mode:
        logger.info(f"[STATE] {old_mode} -> {state.mode}")

    handler = MODE_HANDLERS.get(state.mode, error_step)
    handler(state)

    debug_frame = draw_debug(state)
    if debug_frame is not None:
        cv2.imwrite("debug.jpg", debug_frame)

    apply_output(state)

    logger.info(
        f"[RUN] mode={state.mode} "
        f"reason={state.decision_reason}"
        f"voice_active={state.voice_active}"
        f"voice_cmd={state.voice_command}"
        f"target={state.target_detected} "
        f"lost={state.lost_count} "
        f"obstacle={state.obstacle_detected} "
        f"obstacle_level={state.obstacle_level}"
        f"distance={state.distance_cm} "
        f"cmd={state.move_command} "
        f"speed={state.move_speed} "
        f"pan={state.pan_angle} "
        f"tilt={state.tilt_angle}"
    )
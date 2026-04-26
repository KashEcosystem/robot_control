from logic.memory import memory_is_recent
from core.alert import send_alert

MEMORY_TIME = 1.5
MAX_LOST_COUNT = 8


def decide_mode(state):

    if state.error_message is not None:
        send_alert(f"Robot error: {state.error_message}",
                   level = "ERROR",
                   key = "robot_error")
        return "error"
    if state.obstacle_detected:
        return "avoid_abstacle"
    if state.target_detected:
        return "tracking"
    if memory_is_recent(state, MEMORY_TIME) and state.lost_count <= MAX_LOST_COUNT:
        return "tracking_memory"
    return "scan"
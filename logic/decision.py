from logic.memory import memory_is_recent
from core.alert import send_alert

MEMORY_TIME = 1.5
MAX_LOST_COUNT = 8


def decide_mode(state):

    if state.error_message is not None:
        state.decision_reason = "error_message"
        send_alert(f"Robot error: {state.error_message}",
                   level = "ERROR",
                   key = "robot_error")
        return "error"
    if state.obstacle_detected:
        state.decision_reason = f"obstacle:{state.obstacle_level}"
        return "avoid_abstacle"
    
    if state.target_detected:
        state.decision_reason = "target_detected"
        return "tracking"
    
    if memory_is_recent(state, MEMORY_TIME) and state.lost_count <= MAX_LOST_COUNT:
        state.decision_reason = f"memory_recent lost={state.lost_count} last_dir={state.last_direction}"
        return "tracking_memory"
    
    state.decision_reason = (f"scan: no_target, lost={state.lost_count}, distance={state.distance_cm}")
    return "scan"
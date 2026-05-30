from logic.memory import memory_is_recent
from core.alert import send_alert

MEMORY_TIME = 1.5
MAX_LOST_COUNT = 8


def decide_mode(state):
    """
    Quyết định mode tiếp theo cho robot.

    Decision chỉ đọc RobotState và trả về mode.
    Không gọi motor.
    Không gọi servo.
    Không gọi voice_service.
    """

    # 1. Lỗi hệ thống: ưu tiên cao nhất
    if state.error_message is not None:
        state.decision_reason = "error_message"

        send_alert(
            f"Robot error: {state.error_message}",
            level="ERROR",
            key="robot_error",
        )

        return "error"

    # 2. Vật cản: ưu tiên cao hơn lệnh voice
    if state.obstacle_detected:
        state.decision_reason = f"obstacle:{state.obstacle_level}"
        return "avoid_obstacle"

    # 3. Voice command: stop
    if state.voice_active and state.voice_command == "stop":
        state.decision_reason = "voice:stop"
        return "idle"

    # 4. Voice command: manual movement
    if state.voice_active and state.voice_command in [
        "forward",
        "backward",
        "left",
        "right",
    ]:
        state.decision_reason = f"voice_manual:{state.voice_command}"
        return "manual"

    # 5. Voice command: follow me
    if state.voice_active and state.voice_command == "follow_me":
        if state.target_detected:
            state.decision_reason = "voice_follow:target_detected"
            return "tracking"

        state.decision_reason = "voice_follow:no_target"
        return "scan"

    # 6. Voice command: scan / search
    if state.voice_active and state.voice_command in ["scan", "search"]:
        state.decision_reason = f"voice:{state.voice_command}"
        return "scan"

    # 7. Voice chat: tạm dừng robot khi nói chuyện
    if state.voice_active and state.voice_command == "chat":
        state.decision_reason = "voice:chat_pause_robot"
        return "idle"

    # 8. Vision: thấy mục tiêu
    if state.target_detected:
        state.decision_reason = "target_detected"
        return "tracking"

    # 9. Memory: vừa mất mục tiêu
    if memory_is_recent(state, MEMORY_TIME) and state.lost_count <= MAX_LOST_COUNT:
        state.decision_reason = (
            f"memory_recent lost={state.lost_count} "
            f"last_dir={state.last_direction}"
        )
        return "tracking_memory"

    # 10. Không có gì: scan
    state.decision_reason = (
        f"scan: no_target, lost={state.lost_count}, "
        f"distance={state.distance_cm}"
    )
    return "scan"
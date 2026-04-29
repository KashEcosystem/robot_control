from core.logger_config import logger


def build_voice_response(state) -> str:
    """
    Đọc trạng thái thật của robot rồi tạo câu phản hồi.
    Không quyết định hành động ở đây.
    """

    try:
        if state.mode == "error":
            return "Tôi đang gặp lỗi hệ thống."

        if state.obstacle_detected and state.move_command == "stop":
            return "Tôi đã dừng vì phát hiện vật cản."

        if state.mode == "manual":
            if state.move_command == "forward":
                return "Đang tiến tới."
            if state.move_command == "backward":
                return "Đang lùi lại."
            if state.move_command == "left":
                return "Đang rẽ trái."
            if state.move_command == "right":
                return "Đang rẽ phải."
            if state.move_command == "stop":
                return "Đã dừng lại."
            return "Tôi đang ở chế độ điều khiển bằng giọng nói."

        if state.mode == "scan":
            return "Tôi đang quét tìm mục tiêu."

        if state.mode == "tracking":
            return "Tôi đã thấy mục tiêu và đang theo dõi."

        if state.mode == "idle":
            return "Tôi đang chờ lệnh."

        return "Tôi đang hoạt động."

    except Exception:
        logger.exception("[VOICE_RESPONSE] build response failed")
        return "Tôi không thể tạo phản hồi lúc này."


def speak_response(state) -> None:
    """
    Hiện tại chưa có loa/TTS thật nên chỉ log/print.
    Sau này thay print bằng text-to-speech.
    """

    response = build_voice_response(state)

    logger.info(f"[VOICE_RESPONSE] {response}")
    print(f"ROBOT: {response}")
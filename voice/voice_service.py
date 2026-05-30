from core.logger_config import logger
from voice.voice_input import get_voice_text
from voice.voice_command import parse_voice_command
from voice.ai_response import AIResponse
from voice.tts import speak
from voice.voice_response import build_voice_response
from voice.voice_state import VoiceState


class VoiceService:
    """
    Điều phối toàn bộ voice pipeline:
    - nghe micro
    - parse command
    - gọi AI nếu là câu hỏi
    - phát phản hồi bằng loa

    File này không điều khiển motor/servo trực tiếp.
    """

    def listen_and_process(self) -> VoiceState:
        """
        Nghe người dùng nói.
        Nếu là lệnh robot: trả về VoiceState active=True.
        Nếu là câu hỏi: gọi AI và nói câu trả lời, trả về command='none'.
        """

        text = get_voice_text()

        if not text:
            return VoiceState(
                text="",
                command="none",
                confidence=0.0,
                active=False,
            )

        logger.info(f"[VOICE_SERVICE] heard text={text}")

        voice_state = parse_voice_command(text)

        if voice_state.active:
            logger.info(f"[VOICE_SERVICE] command={voice_state.command}")
            return voice_state

        # Không phải lệnh điều khiển -> xem như câu hỏi giao tiếp
        try:
            answer = AIResponse(text)
            speak(answer)
        except Exception:
            logger.exception("[VOICE_SERVICE] AI response failed")
            speak("Tôi đang bị lỗi kết nối AI.")

            return VoiceState(
                  text=text,
                  command="chat",
                  confidence=1.0,
                  active=True
              )

    def speak_robot_status(self, robot_state) -> None:
        """
        Đọc RobotState rồi phát câu trạng thái ra loa.
        """

        try:
            response = build_voice_response(robot_state)
            logger.info(f"[VOICE_SERVICE] robot status response={response}")
            speak(response)
        except Exception:
            logger.exception("[VOICE_SERVICE] speak robot status failed")
            speak("Tôi không thể đọc trạng thái lúc này.")
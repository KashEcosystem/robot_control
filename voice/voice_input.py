import speech_recognition as sr
from core.logger_config import logger


MIC_DEVICE_INDEX = 1


def get_voice_text(language: str = "vi-VN") -> str:
    recognizer = sr.Recognizer()

    recognizer.energy_threshold = 150
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8

    try:
        with sr.Microphone(device_index=MIC_DEVICE_INDEX) as source:
            print("Im lặng 1 giây...")
            recognizer.adjust_for_ambient_noise(source, duration=1)

            print("Nói lệnh bây giờ...")
            audio = recognizer.listen(
                source,
                timeout=12,
                phrase_time_limit=5
            )

        print("Đang nhận diện...")
        text = recognizer.recognize_google(audio, language=language)
        return text.strip().lower()

    except sr.WaitTimeoutError:
        print("Không nghe thấy tiếng nói.")
        return ""

    except sr.UnknownValueError:
        print("Có âm thanh nhưng không hiểu rõ.")
        return ""

    except sr.RequestError as e:
        print("Lỗi internet hoặc Google Speech:", e)
        return ""

    except Exception:
        logger.exception("[VOICE_INPUT] unexpected error")
        print("Lỗi voice input.")
        return ""
    
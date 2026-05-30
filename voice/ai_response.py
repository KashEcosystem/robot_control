import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from voice.robot_profile import ROBOT_INTRO, ROBOT_SYSTEM_PROMPT

system_instruction=ROBOT_SYSTEM_PROMPT
load_dotenv()


class AIResponse:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

        if not self.api_key:
            raise ValueError("Missing GEMINI_API_KEY in .env")

        self.client = genai.Client(api_key=self.api_key)

    def ask(self, text: str) -> str:
        if not text or not text.strip():
            return "Tôi chưa nghe rõ, bạn nói lại được không?"

        text = text.lower().strip()

        intro_questions = [
             "bạn là ai",
             "mày là ai",
             "kash là ai",
             "robot kash là gì",
             "giới thiệu bản thân",
             "giới thiệu về bạn",
        ]

        if any(q in text for q in intro_questions):
            return ROBOT_INTRO
  
        try:
            response = self.client.models.generate_content(
               model=self.model,
               contents=text,
               config=types.GenerateContentConfig(
                     system_instruction=ROBOT_SYSTEM_PROMPT,
                     temperature=0.4,
            ),
        )

            if not response.text:
                 return "Tôi chưa có câu trả lời."

            return response.text.strip()

        except Exception as e:
            print(f"[AI Gemini Error] {e}")
            return "Gemini đang bận. Bạn thử hỏi lại sau một chút."
from dataclasses import dataclass

@dataclass
class VoiceState:
    text: str = ""
    command:str = "none"
    confidence: float = 0.0
    active: bool = False
    
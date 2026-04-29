from dataclasses import dataclass
from typing import Optional
from core.config import (PAN_DEFAULT, TILT_DEFAULT, SCAN_DIRECTION, FRAME_WIDTH, FRAME_HEIGHT)

@dataclass
class RobotState:
    mode:str = "idle"
    error_message:Optional[str] = "error"

    frame = None
    frame_width:int = FRAME_WIDTH
    frame_height:int = FRAME_HEIGHT

    target_detected: bool = False
    target_x:int = 0
    target_y:int = 0
    target_area: float = 0.0 
    lost_count: int = 0   

    move_command:str = "stop"
    move_speed: int = 0
    prev_speed: int = 0

    pan_angle:int = PAN_DEFAULT
    tilt_angle:int = TILT_DEFAULT
    scan_direction:int = SCAN_DIRECTION

    offset_x:int = 0
    offset_y:int = 0

    obstacle_detected: bool = False
    distance_cm: float = 999.0
    
    last_seen_time: float = 0.0
    last_direction: str = "center"
    last_move_command: str = "stop"
    last_move_speed: int = 0
    camera_fail_count: int = 0
    trace_id = 0
    decision_reason: str = ""
    action_reason: str = ""
    obstacle_level: str = "clear"

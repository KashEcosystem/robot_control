from core.logger_config import logger
from core.config import MODE
 

def apply_output(state):

    try:
        if MODE == "SIMULATION":
            logger.info(f"[SIM] pan={state.pan_angle} tilt={state.tilt_angle} cmd={state.move_command} speed={state.move_speed}")
            return
        
        elif MODE == "SAFE":
            from hardware import servo, motor
            safe_pan = max(60, min(140, state.pan_angle))
            safe_tilt = max(70, min(110, state.tilt_angle))
            servo.set_pan(safe_pan)
            servo.set_tilt(safe_tilt)
            motor.apply_motor_command(state.move_command, state.move_speed)

            logger.info(f"[SAFE] pan={state.pan_angle} tilt={state.tilt_angle} cmd={state.move_command} move={state.move_speed} ")
            return

        elif MODE == "PRODUCTION":
            from hardware import servo, motor
            logger.info(f"[PRODUCTION] pan={state.pan_angle} tilt={state.tilt_angle} cmd={state.move_command} speed={state.move_speed}")
            servo.set_pan(state.pan_angle)
            servo.set_tilt(state.tilt_angle)
            motor.apply_motor_command(state.move_command, state.move_speed)
            return
        
        else:
            logger.warning(f"[CONFIG] Unknown MODE={MODE}")
            
    except Exception:
        logger.exception(f"[OUTPUT ERROR] hardware failure")
        state.mode = "error"
        state.move_command = "stop"
        state.move_speed = 0
        try:
            motor.stop()
        except Exception:
            pass
         
        

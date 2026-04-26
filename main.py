from core.logger_config import logger
from core.config import DELAY,MODE
from state.robot_state import RobotState
from logic.controller import run_step
from hardware.camera import init_camera
import time

def main():
    logger.info(f"[MAIN] robot start")
    state = RobotState()
    init_camera()

    try:
        while True:
            run_step(state)
            time.sleep(DELAY)
    except KeyboardInterrupt:
        logger.warning(f"[MAIN] keyboard interrupt robot stoping")
    except Exception:
        logger.exception(f"[MAIN] error main loop")


    finally:
        logger.info(f"[MAIN] cleanup start")
        try:
            if MODE != "SIMULATION":
               from hardware import motor, servo, camera
            
               motor.cleanup()
               servo.cleanup()
               camera.cleanup()
        except Exception:
            logger.exception(f'[MAIN] cleanup failed')

        logger.info(f'[MAIN] robot stopped')

if __name__=="__main__":
    main()


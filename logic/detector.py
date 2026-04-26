import numpy as np
import cv2
from core.logger_config import logger
from core.config import MIN_TARGET_AREA

def detect_target(state):
    frame = state.frame

    if frame is None:
        state.target_detected = False
        state.target_x = 0
        state.target_y = 0
        state.tafget_area = 0.0
        logger.warning(f"[DETECT] frame is None -> no target")
        return
    try:
        blurred = cv2.GaussianBlur(frame, (5,5), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        print("[HSV CENTER]", hsv[240][320])

        
        lower_target = np.array([55, 80, 40])
        upper_target = np.array([80, 255, 120])
        mask = cv2.inRange(hsv, lower_target, upper_target)
    

        kernel = np.ones((5,5), np.uint8)
        mask = cv2.erode(mask, kernel, iterations = 1)
        mask = cv2.dilate(mask, kernel, iterations = 2)
        cv2.imwrite("mask.jpg", mask)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            state.target_detected = False
            state.target_x = 0
            state.target_y = 0
            state.target_area = 0.0
            logger.warning(f"[DETECT] no contours -> no target")
            return
        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)
        if area < MIN_TARGET_AREA:
            state.target_detected = False
            state.target_x = 0
            state.target_y = 0
            state.target_area = 0.0
            logger.warning(f"[DETECT] contour too small, area={area}")
            return
        
        x,y,w,h = cv2.boundingRect(largest_contour)
        state.target_detected = True
        state.target_x = x + w // 2
        state.target_y = y + h // 2
        state.target_area = float (area)
        logger.info(f"[DETECT] x={state.target_x} y={state.target_y} area={state.target_area}")

    except Exception as e:
        state.target_detected = False
        state.target_x = 0
        state.target_y = 0
        state.target_area = 0.0
        state.error_message = f"detect_target error: {e}"
        logger.exception(f"[DETECT] exception while detecting target")

import cv2


def draw_debug(state):
    if state.frame is None:
        return None

    frame = state.frame.copy()

    # ===== BASIC STATUS =====
    cv2.putText(
        frame,
        f"mode={state.mode} cmd={state.move_command} speed={state.move_speed}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )

    # ===== CAMERA CENTER =====
    center_x = state.frame_width // 2
    center_y = state.frame_height // 2

    cv2.circle(frame, (center_x, center_y), 6, (255, 0, 0), -1)

    cv2.line(frame, (center_x, 0), (center_x, state.frame_height), (255, 0, 0), 1)
    cv2.line(frame, (0, center_y), (state.frame_width, center_y), (255, 0, 0), 1)

    # ===== TARGET INFO =====
    if state.target_detected:
        cv2.circle(frame, (state.target_x, state.target_y), 8, (0, 0, 255), -1)

        cv2.line(
            frame,
            (center_x, center_y),
            (state.target_x, state.target_y),
            (0, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"target=({state.target_x},{state.target_y}) area={int(state.target_area)}",
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"error_x={state.offset_x} error_y={state.offset_y}",
            (10, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 255),
            2
        )
    else:
        cv2.putText(
            frame,
            "target=False",
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 0, 255),
            2
        )

    # ===== OBSTACLE INFO =====
    cv2.putText(
        frame,
        f"obstacle={state.obstacle_detected} distance={state.distance_cm}",
        (10, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 0),
        2
    )

    # ===== SERVO INFO =====
    cv2.putText(
        frame,
        f"pan={state.pan_angle} tilt={state.tilt_angle}",
        (10, 150),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 0),
        2
    )

    return frame
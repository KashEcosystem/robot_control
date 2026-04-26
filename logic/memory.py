import time

def update_memory(state):
    
    if state.target_detected:
        state.last_seen_time = time.time()
        state.lost_count = 0
        center_x = state.frame_width // 2

        if state.target_x > center_x:
            state.last_direction = "right"
        elif state.target_x < center_x:
            state.last_direction = "left"
        else:
            state.last_direction = "center"
        state.last_move_command = state.move_command
        state.last_move_speed = state.move_speed
    else:
        state.lost_count += 1


def memory_is_recent(state, max_second: float = 1.5) -> bool:

    if state.last_seen_time <= 0:
        return False
    return time.time() - state.last_seen_time <= max_second
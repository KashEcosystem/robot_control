def avoid_obstacle(state):
    if state.distance < 20:
         state.move_command = "left"
    else:
         state.move_command = "forward"
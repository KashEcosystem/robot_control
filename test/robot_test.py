from sensor_fake import get_distance
from avoid import avoid_obstacle
from core.config import MODE
import time

class State:
    def __init__(self):
        self.distance = 100
        self.move_command = "stop"

state = State()

while True:
    if MODE=="SIMULATION":
        state.distance = get_distance()

    else:
        state.distance = 10
    avoid_obstacle(state)

    print(f"Distance: {state.distance} -> {state.move_command}")
    time.sleep(0.8)
import time
from core.logger_config import logger

TRACE_ENABLED = True

class RobotTrace:
    def __init__(self,state):
        self.state = state
        self.step_id = 0
        self.start_time = time.time()
        self.last_step_time = self.start_time

        self.state.trace_id += 1
        self.trace_id = self.state.trace_id

    def step (self, name:str, extra: str= ""):
        if not TRACE_ENABLED:
            return
        
        now = time.time()
        step_time = now - self.last_step_time
        total_time = now - self.last_step_time
        self.last_step_time = now
        self.step_id += 1

        logger.debug(f"[TRACE {self.trace_id:04}]"
                     f"[STEP {self.step_id:02}]"
                     f"{name} {extra}"
                     f" | step={step_time:.3f}s total= {total_time:3f}s"
                     )
        def done(self):
            if not TRACE_ENABLED:
                return
            
            total_time = time.time() - self.start_time 
            logger.debug(f"[TRACE {self.trace_id:04}] DONE | total={total_time:.3f}s")
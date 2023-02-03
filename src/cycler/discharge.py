from src.cycler.base import BaseCycler

class Discharge(BaseCycler):
    cycle_steps = ['discharge']

    def __init__(self, discharge_current, V_min):
        super().__init__()
        self.discharge_current = -discharge_current
        self.V_min = V_min
        self.num_cycles = 1

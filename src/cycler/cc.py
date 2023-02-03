from src.cycler.base import BaseCycler


class CC(BaseCycler):
    # class variables
    cycle_steps = ["rest", "charge", "rest", "discharge"]

    def __init__(self, num_cycles, charge_current, discharge_current, rest_time, V_max, V_min):
        super().__init__()
        self.num_cycles = num_cycles
        self.charge_current = charge_current
        self.discharge_current = -discharge_current
        self.rest_time = rest_time
        self.V_max = V_max
        self.V_min = V_min
        # self.time_elapsed = 0.0
    #
    # def get_current(self, step_name):
    #     if step_name == "rest":
    #         return 0.0
    #     elif step_name == "charge":
    #         return self.charge_current
    #     elif step_name == "discharge":
    #         return self.discharge_current
    #     else:
    #         raise TypeError("Not a valid step name")
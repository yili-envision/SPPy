from SPPy.cycler.base import BaseCycler


class Charge(BaseCycler):

    def __init__(self, charge_current: float, V_max: float, SOC_LIB_max: float=1, SOC_LIB: float=0):
        super().__init__(charge_current=charge_current, SOC_LIB_max=SOC_LIB_max)
        # self.charge_current = charge_current
        self.V_max = V_max
        self.num_cycles = 1
        # self.SOC_max = SOC_max
        self.SOC_LIB = SOC_LIB
        self.cycle_steps = ['charge']
        self.SOC_LIB_init = SOC_LIB

    def get_current(self, step_name: str, t: float = 0.0) -> float:
        return self.charge_current

    def reset(self) -> None:
        self.time_elapsed = 0.0
        self.SOC_LIB = self.SOC_LIB_init


class ChargeRest(BaseCycler):
    def __init__(self, charge_current: float, V_max:float, rest_time: float, SOC_LIB_max:float=1, SOC_LIB:float=0):
        super().__init__(charge_current=charge_current, SOC_LIB_max=SOC_LIB_max, SOC_LIB=SOC_LIB)
        self.cycle_steps = ['charge', 'rest']
        self.rest_time = rest_time
        self.num_cycles = 1
        self.V_max = V_max
        self.SOC_LIB_init = SOC_LIB

    def get_current(self, step_name: str, t: float = 0.0) -> float:
        if step_name == 'charge':
            return self.charge_current
        elif step_name == 'rest':
            return 0

    def reset(self) -> None:
        self.time_elapsed = 0.0
        self.SOC_LIB = self.SOC_LIB_init

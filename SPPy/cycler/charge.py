from SPPy.cycler.base import BaseCycler


class Charge(BaseCycler):
    cycle_steps = ['charge']

    def __init__(self, charge_current, V_max, SOC_max=1, SOC_LIB=0):
        super().__init__()
        self.charge_current = charge_current
        self.V_max = V_max
        self.num_cycles = 1
        self.SOC_max = SOC_max
        self.SOC_LIB=SOC_LIB
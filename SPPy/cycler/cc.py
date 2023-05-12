from SPPy.cycler.base import BaseCycler


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

class CCNoFirstRest(BaseCycler):
    # class variables
    cycle_steps = ["charge", "rest", "discharge", "rest"]

    def __init__(self, num_cycles, charge_current, discharge_current, rest_time, V_max, V_min, SOC_min=0, SOC_max=1,
                 SOC_LIB=0):
        super().__init__()
        self.num_cycles = num_cycles
        self.charge_current = charge_current
        self.discharge_current = -discharge_current
        self.rest_time = rest_time
        self.V_max = V_max
        self.V_min = V_min
        self.SOC_min = SOC_min
        self.SOC_max = SOC_max
        self.SOC_LIB = SOC_LIB

class CCCV(BaseCycler):
    # class variables
    cycle_steps = ["charge", "CV", "rest", "discharge", "rest"]

    def __init__(self, num_cycles, charge_current, discharge_current, rest_time, V_max, V_min, SOC_min=0, SOC_max=1,
                 SOC_LIB=0):
        super().__init__()
        self.num_cycles = num_cycles
        self.charge_current = charge_current
        self.discharge_current = -discharge_current
        self.rest_time = rest_time
        self.V_max = V_max
        self.V_min = V_min
        self.SOC_min = SOC_min
        self.SOC_max = SOC_max
        self.SOC_LIB = SOC_LIB
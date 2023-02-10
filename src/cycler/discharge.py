import numpy as np

from src.cycler.base import BaseCycler

class Discharge(BaseCycler):
    cycle_steps = ['discharge']

    def __init__(self, discharge_current, V_min, SOC_min, SOC_LIB):
        super().__init__()
        self.discharge_current = -discharge_current
        self.V_min = V_min
        self.num_cycles = 1
        self.SOC_min = SOC_min
        self.SOC_LIB = SOC_LIB

class DischargeRest(BaseCycler):
    cycle_steps = ['discharge', 'rest']

    def __init__(self, discharge_current, rest_time, V_min):
        super().__init__()
        self.discharge_current = -discharge_current
        self.rest_time = rest_time
        self.V_min = V_min
        self.num_cycles = 1


class CustomDischarge(BaseCycler):
    cycle_steps = ['discharge']

    def __init__(self, t_array, I_array, V_min):
        # Check for input type.
        if not isinstance(t_array, np.ndarray):
            raise TypeError("t_array needs to be a numpy array.")
        if not isinstance(I_array, np.ndarray):
            raise TypeError("I_array needs to be a numpy array.")
        # Check is the size of the time and current arrays are equal
        if len(t_array) != len(I_array):
            raise ValueError("t_array and I_array needs to be of the same length.")
        super().__init__()
        self.t_array = t_array
        self.I_array = -I_array
        self.V_min = V_min
        self.num_cycles = 1

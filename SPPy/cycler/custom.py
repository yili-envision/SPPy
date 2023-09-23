import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from scipy import interpolate
from SPPy.cycler.base import BaseCycler


class CustomCycler(BaseCycler):
    def __init__(self, array_t: npt.ArrayLike, array_I: npt.ArrayLike, V_min: float, V_max: float,
                 SOC_LIB: float=1.0, SOC_LIB_min: float=0.0, SOC_LIB_max: float=1.0):
        """
        CustomCycler constructor.
        :param t_array: numpy array containing the time values in sequence [s].
        :param I_array: numpy array containing the current values.
        :param SOC_LIB:
        """
        super().__init__(SOC_LIB=SOC_LIB, SOC_LIB_min=SOC_LIB_min, SOC_LIB_max=SOC_LIB_max)
        # check is t_array and I_array are numpy arrays.
        if (not isinstance(array_t, np.ndarray)) and (not isinstance(array_I, np.ndarray)):
            raise TypeError("t_array and I_array needs to be a numpy array.")

        # t_array and I_array needs to be of equal sizes
        if array_t.shape[0] != array_I.shape[0]:
            raise ValueError("t_array and I_array are not of equal sizes.")

        self.array_t = array_t
        self.array_I = array_I
        self.cycle_steps = ['custom']
        self.SOC_LIB_init = self.SOC_LIB
        self.V_min = V_min
        self.V_max = V_max

    @property
    def t_max(self):
        """
        Returns the time value at the last iteration.
        :return: (float) time value at the last iteration
        """
        return self.array_t[-1]

    def get_current(self, step_name: str, t: float):
        """
        Returns the current value from the inputted time value. This current value is interpolation based on the
        current value at the previous time step.
        :param step_name: cycling step name
        :param t: time [s]
        :returns: current value [A]
        """
        return interpolate.interp1d(self.array_t, self.array_I, kind='previous', fill_value='extrapolate')(t)

    def reset(self) -> None:
        self.time_elapsed = 0.0
        self.SOC_LIB = self.SOC_LIB_init

    def plot(self):
        """
        Plots the cycler's instance time [s] vs. current [A]. According to the convention, the discharge current is
        negative.
        :return:
        """
        plt.plot(self.array_t, self.array_I)
        plt.xlabel('Time [s]')
        plt.ylabel('I [A]')
        plt.show()




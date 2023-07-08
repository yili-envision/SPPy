import numpy as np
import numpy.typing as npt
from scipy import interpolate
from SPPy.cycler.base import BaseCycler


class CustomCycler(BaseCycler):
    def __init__(self, t_array: npt.ArrayLike, I_array: npt.ArrayLike):
        # check is t_array and I_array are numpy arrays.
        if (not isinstance(t_array, np.ndarray)) and (not isinstance(I_array, np.ndarray)):
            raise TypeError("t_array and I_array needs to be a numpy array.")

        # t_array and I_array needs to be of equal sizes
        if t_array.shape[0] != I_array.shape[0]:
            raise ValueError("t_array and I_array are not of equal sizes.")

        self.t_array = t_array
        self.I_array = I_array

    def get_current(self, t: float):
        """
        Returns the current value from the inputted time value. This current value is interpolation based on the
        current value at the previous time step.
        :param t: time [s]
        :returns: current value [A]
        """
        return interpolate.interp1d(self.t_array, self.I_array, kind='previous', fill_value='extrapolate')(t)
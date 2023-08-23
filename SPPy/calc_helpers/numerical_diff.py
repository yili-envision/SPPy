import numpy
import numpy as np
import numpy.typing as npt


def first_centered_FD(array_x: npt.ArrayLike, array_t: npt.ArrayLike) -> npt.ArrayLike:
    """
    calculates the first order differential using centered finite difference of the equation:
    :param array_x: x value at the x step
    :param array_t: t value at the t step
    :return: array containing the differential values.
    """
    array_diff = np.zeros(len(array_t)-2)
    for i in range(1, len(array_diff)+1):
        array_diff[i-1] = (array_x[i+1] - array_x[i-1]) / (array_t[i+1] - array_t[i-1])
    return array_diff
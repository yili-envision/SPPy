import numpy as np


def calc_mse(array1, array2):
    """
    Calcs the mse of two numpy array
    :param array1: numpy array of observed values.
    :param array2: numpy array of predicted values.
    :return: mean squared error of the two arrays.
    """
    # check for input types
    if not isinstance(array1, np.ndarray):
        raise TypeError("mse array 1 input needs to be a numpy array object.")
    if not isinstance(array2, np.ndarray):
        raise TypeError("mse array 2 input needs to be a numpy array object.")
    return np.mean(np.square(array1 - array2))

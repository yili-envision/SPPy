import unittest
import numpy as np

from src.calc_helpers import errors


class TestErrors(unittest.TestCase):

    def test_mse(self):
        arr1 = np.array([1,2,3,4])
        arr2 = np.array([2,3,4,5])
        print(errors.calc_mse(arr1, arr2))
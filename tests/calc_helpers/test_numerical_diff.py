import unittest

import numpy as np

from SPPy.calc_helpers.numerical_diff import first_centered_FD


class TestFirstCenteredFD(unittest.TestCase):
    def test_sin_func(self):
        t = np.linspace(0, 2 * np.pi)
        x = np.sin(t)
        dxdt = first_centered_FD(array_x=x, array_t=t)
        # print(x)
        # print(t)
        print(dxdt)
        self.assertEqual(len(t)-2, len(dxdt))
        self.assertAlmostEqual(2.53654584e-01 / 0.25645654, dxdt[0])

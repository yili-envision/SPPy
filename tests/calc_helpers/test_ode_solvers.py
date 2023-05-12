import unittest
import numpy as np

from SPPy.calc_helpers.ode_solvers import euler, rk4


class TestEuler(unittest.TestCase):

    def test_euler(self):
        def func(y, t):
            return 4*np.exp(0.8*t) - 0.5*y
        t_array = np.arange(0, 5)
        y_array = np.zeros(len(t_array))
        y_array[0] = 2.0
        for i in range(1,len(t_array)):
            t_prev = t_array[i-1]
            y_prev = y_array[i-1]
            dt = t_array[i]-t_array[i-1]
            y_array[i] = euler(func=func, t_prev=t_prev, y_prev=y_prev, step_size=dt)
        self.assertEqual(y_array[1], 5.0)
        self.assertEqual(y_array[2], 11.402163713969871)
        self.assertEqual(y_array[3], 25.513211554565395)
        self.assertEqual(y_array[4], 56.84931129984912)

    def test_rk4(self):
        def func(y, t):
            return 4*np.exp(0.8*t) - 0.5*y
        t_prev = 0.0
        y_prev = 2.0
        dt = 1.0
        self.assertEqual(rk4(func=func, t_prev=t_prev, y_prev=y_prev, step_size=dt), 6.201037072414292)

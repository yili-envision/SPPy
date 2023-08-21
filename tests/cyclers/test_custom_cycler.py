import unittest
import numpy as np

from SPPy.cycler.custom import CustomCycler


class TestCustomCycler(unittest.TestCase):
    t_array = np.arange(5)
    I_array = np.array([-1.656, 0, -1.656, 0, -2*1.656])

    def test_constructor1(self):
        cycler = CustomCycler(t_array=self.t_array, I_array=self.I_array)
        self.assertEqual(0.0, cycler.time_elapsed)
        self.assertEqual(0.0, cycler.SOC_LIB)

        self.assertTrue(np.array_equal(self.t_array, cycler.t_array))
        self.assertTrue(np.array_equal(self.I_array, cycler.I_array))

        with self.assertRaises(ValueError) as context:
            CustomCycler(t_array=self.t_array, I_array=np.array([0]))

    def test_constructor2(self):
        cycler = CustomCycler(t_array=self.t_array, I_array=self.I_array, SOC_LIB=1.0)
        self.assertEqual(0.0, cycler.time_elapsed)
        self.assertEqual(1.0, cycler.SOC_LIB)

        self.assertTrue(np.array_equal(self.t_array, cycler.t_array))
        self.assertTrue(np.array_equal(self.I_array, cycler.I_array))


    def test_get_current_method(self):
        cycler = CustomCycler(t_array=self.t_array, I_array=self.I_array)
        self.assertEqual(self.I_array[0], cycler.get_current(t=0))
        self.assertEqual(self.I_array[0], cycler.get_current(t=0.1))
        self.assertEqual(self.I_array[0], cycler.get_current(t=0.2))
        self.assertEqual(self.I_array[0], cycler.get_current(t=0.3))
        self.assertEqual(self.I_array[0], cycler.get_current(t=0.5))
        self.assertEqual(self.I_array[0], cycler.get_current(t=0.7))
        self.assertEqual(self.I_array[0], cycler.get_current(t=0.9))

        self.assertEqual(self.I_array[1], cycler.get_current(t=1))
        self.assertEqual(self.I_array[1], cycler.get_current(t=1.5))
        self.assertEqual(self.I_array[1], cycler.get_current(t=1.99))

        self.assertEqual(self.I_array[-2], cycler.get_current(t=3))
        self.assertEqual(self.I_array[-2], cycler.get_current(t=3.5))
        self.assertEqual(self.I_array[-2], cycler.get_current(t=3.99))

        self.assertEqual(self.I_array[-1], cycler.get_current(t=4.1))





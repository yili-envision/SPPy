import unittest

from SPPy.sol_and_visualization.solution import SolutionInitializer


class TestSolutionInitializer(unittest.TestCase):
    def test_constructor(self):
        """
        Tests for default values in case of class initialization.
        """
        sol = SolutionInitializer()
        self.assertEqual([], sol.lst_cycle_num)
        self.assertEqual([], sol.lst_cycle_step)
        self.assertEqual([], sol.lst_t)
        self.assertEqual([], sol.lst_I)
        self.assertEqual([], sol.lst_V)
        self.assertEqual([], sol.lst_x_surf_p)
        self.assertEqual([], sol.lst_x_surf_n)
        self.assertEqual([], sol.lst_cap)
        self.assertEqual([], sol.lst_cap_charge)
        self.assertEqual([], sol.lst_cap_discharge)
        self.assertEqual([], sol.lst_battery_cap)
        self.assertEqual([], sol.lst_temp)
        self.assertEqual([], sol.lst_R_cell)
        self.assertEqual([], sol.lst_j_tot)
        self.assertEqual([], sol.lst_j_i)
        self.assertEqual([], sol.lst_j_s)
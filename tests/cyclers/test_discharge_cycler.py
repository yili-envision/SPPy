import unittest

from src.cycler.discharge import Discharge


class TestDischargeCycler(unittest.TestCase):
    def test_constructor(self):
        discharge_current = 1.5
        V_min = 2.5
        dc = Discharge(discharge_current=discharge_current, V_min=V_min)
        self.assertEqual(-discharge_current, dc.discharge_current)
        self.assertEqual(V_min, dc.V_min)
        self.assertEqual(0.0, dc.time_elapsed)
        self.assertEqual('discharge', dc.cycle_steps[0])

    def test_get_current(self):
        discharge_current = 1.5
        V_min = 2.5
        dc = Discharge(discharge_current=discharge_current, V_min=V_min)
        self.assertEqual(-discharge_current,dc.get_current(dc.cycle_steps[0]))
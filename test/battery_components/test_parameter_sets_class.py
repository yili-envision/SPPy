import unittest
import os

from SPPy.battery_components.battery_cell import ParameterSets


class TestParameterSetsBasic(unittest.TestCase):
    def test_constructor_with_valid_name(self):
        params = ParameterSets(name='test')
        self.assertEqual('test', params.name)
        self.assertEqual(os.path.basename('..\\..\\parameter_sets\\test\\param_electrolyte.csv'),
                         os.path.basename(params.ELECTROLYTE_DIR))



    def test_constructor_with_invalid_name(self):
        with self.assertRaises(ValueError) as context:
            ParameterSets('non-sense')

class TestParameterSetsMethods(unittest.TestCase):
    def test_list_parameter_sets_methods(self):
        self.assertTrue(self.check_for_parameter_sets('test'))

    def check_for_parameter_sets(self, *args):
        for parameter_set_name in args:
            if parameter_set_name not in ParameterSets.list_parameters_sets():
                return False
        return True

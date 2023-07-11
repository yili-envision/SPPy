import importlib

import pandas as pd

from SPPy.config.definations import *


class ParameterSets:
    PARAMETER_SET_DIR = PARAMETER_SET_DIR  # directory to the parameter_sets folder

    def __init__(self, name: str):
        self.check_parameter_set(name)  # checks if the inputted name is available in the parameter sets.
        self.name = name  # name of the parameter set

        self.POSITIVE_ELECTRODE_DIR = os.path.join(self.PARAMETER_SET_DIR, self.name, 'param_pos-electrode.csv')
        self.NEGATIVE_ELECTRODE_DIR = os.path.join(self.PARAMETER_SET_DIR, self.name, 'param_neg-electrode.csv')
        self.ELECTROLYTE_DIR = os.path.join(self.PARAMETER_SET_DIR, self.name, 'param_electrolyte.csv')
        self.BATTERY_CELL_DIR = os.path.join(self.PARAMETER_SET_DIR, self.name, 'param_battery-cell.csv')

        func_module = importlib.import_module(f'parameter_sets.{self.name}.funcs')  # imports the python module
        # containing the OCP related funcs in the parameter set.
        self.OCP_ref_p_ = func_module.OCP_ref_p
        self.dOCPdT_p_ = func_module.dOCPdT_p
        self.OCP_ref_n_ = func_module.OCP_ref_n
        self.dOCPdT_n_ = func_module.dOCPdT_n

    @classmethod
    def list_parameters_sets(cls):
        """
        Returns the list of available parameter sets.
        :return: (list) list of available parameters sets.
        """
        return os.listdir(cls.PARAMETER_SET_DIR)

    @classmethod
    def check_parameter_set(cls, name):
        """
        Checks if the inputted parameter name is in the parameter set. If not available, it raises an exception.
        """
        if name not in cls.list_parameters_sets():
            raise ValueError(f'{name} no in parameter sets.')

    @classmethod
    def parse_csv(cls, file_path):
        """
        reads the csv file and returns a Pandas DataFrame.
        :param file_path: the absolute or relative file drectory of the csv file.
        :return: the dataframe with the column containing numerical values only.
        """
        return pd.read_csv(file_path, index_col=0)["Value"]

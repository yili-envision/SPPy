""" parameters_set
Contains the classes and functionality for the extracting battery cell parameters
"""

__all__ = ['ParameterSets']

__author__ = 'Moin Ahmed'
__copywrite__ = 'Copywrite 2023 by Moin Ahmed. All rights reserved'
__status__ = 'deployed'


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

        # Positive electrode parameters are extracted below
        df = ParameterSets.parse_csv(file_path=self.POSITIVE_ELECTRODE_DIR)  # Read and parse the csv file.
        self.L_p = df['Electrode Thickness [m]']
        self.A_p = df['Electrode Area [m^2]']
        self.kappa_p = df['Ionic Conductivity [S m^-1]']
        self.epsilon_p = df['Volume Fraction']
        self.max_conc_p = df['Max. Conc. [mol m^-3]']
        self.R_p = df['Radius [m]']
        self.S_p = df['Electroactive Area [m^2]']
        self.T_ref_p = df['Reference Temperature [K]']
        self.D_ref_p = df['Reference Diffusitivity [m^2 s^-1]']
        self.k_ref_p = df['Reference Rate Constant [m^2.5 mol^-0.5 s^-1]']
        self.Ea_D_p = df['Activation Energy of Diffusion [J mol^-1]']
        self.Ea_R_p = df['Activation Energy of Reaction [J mol^-1]']
        self.alpha_p = df['Anodic Transfer Coefficient']
        self.brugg_p = df['Bruggerman Coefficient']

        # Negative electrode parameters are extracted below
        df = ParameterSets.parse_csv(file_path=self.NEGATIVE_ELECTRODE_DIR)  # Read and parse the csv file.
        self.L_n = df['Electrode Thickness [m]']
        self.A_n = df['Electrode Area [m^2]']
        self.kappa_n = df['Ionic Conductivity [S m^-1]']
        self.epsilon_n = df['Volume Fraction']
        self.max_conc_n = df['Max. Conc. [mol m^-3]']
        self.R_n = df['Radius [m]']
        self.S_n = df['Electroactive Area [m^2]']
        self.T_ref_n = df['Reference Temperature [K]']
        self.D_ref_n = df['Reference Diffusitivity [m^2 s^-1]']
        self.k_ref_n = df['Reference Rate Constant [m^2.5 mol^-0.5 s^-1]']
        self.Ea_D_n = df['Activation Energy of Diffusion [J mol^-1]']
        self.Ea_R_n = df['Activation Energy of Reaction [J mol^-1]']
        self.alpha_n = df['Anodic Transfer Coefficient']
        self.brugg_n = df['Bruggerman Coefficient']
        # SEI parameters for the negative electrode are extracted below
        self.U_s = df['SEI Reference Overpotential [V]']
        self.i_s = df['SEI Exchange Current Density [A m^-1]']
        self.MW_SEI = df['SEI Molar Weight [kg mol^-1]']
        self.rho_SEI = df['SEI Density [kg m^-3]']
        self.kappa_SEI = df['SEI Conductivity [S m^-1]']  # SEI conductivity [S/m]

        # Below extracts electrolyte parameters
        df = ParameterSets.parse_csv(file_path=self.ELECTROLYTE_DIR)
        self.conc_es = df['Conc. [mol m^-3]']
        self.L_es = df['Thickness [m]']
        self.kappa_es = df['Ionic Conductivity [S m^-1]']
        self.epsilon_es = df['Volume Fraction']
        self.brugg_es = df['Bruggerman Coefficient']

        # Below extracts the battery cell parameters
        df = ParameterSets.parse_csv(file_path=self.BATTERY_CELL_DIR)
        self.rho = df['Density [kg m^-3]']
        self.Vol = df['Volume [m^3]']
        self.C_p = df['Specific Heat [J K^-1 kg^-1]']
        self.h = df['Heat Transfer Coefficient [J s^-1 K^-1]']
        self.A = df['Surface Area [m^2]']
        self.cap = df['Capacity [A hr]']
        self.V_max = df['Maximum Potential Cut-off [V]']
        self.V_min = df['Minimum Potential Cut-off [V]']

        func_module = importlib.import_module(f'parameter_sets.{self.name}.funcs')  # imports the python module
        # containing the OCP related funcs in the parameter set.
        self.OCP_ref_p_ = func_module.OCP_ref_p
        self.dOCPdT_p_ = func_module.dOCPdT_p
        self.OCP_ref_n_ = func_module.OCP_ref_n
        self.dOCPdT_n_ = func_module.dOCPdT_n
        # containing the electrolyte related fuctions in the parameter set below.
        try:
            self.func_D_e_ = func_module.func_D_e
        except AttributeError as e:
            print('No electrolyte related functions found in the parameter set.')
            self.func_D_e_ = None

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

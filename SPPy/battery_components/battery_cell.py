from dataclasses import dataclass
from typing import Callable
import importlib

from SPPy.config.definations import *
from SPPy.battery_components import electrolyte, electrode


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


@dataclass
class BatteryCellBase:
    T_: float  # battery cell temperature, K
    rho: float  # battery density (mostly for thermal modelling), kg/m3
    Vol: float  # battery cell volume, m3
    C_p: float  # specific heat capacity, J / (K kg)
    h: float  # heat transfer coefficient, J / (S K)
    A: float  # surface area, m2
    cap: float  # capacity, Ah
    V_max: float  # maximum potential
    V_min: float  # minimum potential

    elec_p: electrode.PElectrode  # electrode class object
    elec_n: electrode.NElectrode  # electrode class object
    electrolyte: electrolyte.Electrolyte  # electrolyte class object

    def __post_init__(self):
        # self.T_ = self.T
        self.T_amb_ = self.T  # initial condition
        # initialize internal cell resistance
        self.R_cell = (self.elec_p.L / self.elec_p.kappa_eff + self.electrolyte.L / self.electrolyte.kappa_eff + \
                       self.elec_n.L / self.elec_n.kappa_eff) / self.elec_n.A
        self.R_cell_init = self.R_cell

    @property
    def T(self):
        return self.T_

    @T.setter
    def T(self, new_T):
        self.T_ = new_T
        self.elec_p.T = new_T
        self.elec_n.T = new_T

    @property
    def T_amb(self):
        return self.T_amb_


class BatteryCell(BatteryCellBase):
    """
    Class for the BatteryCell object and contains the relevant parameters.
    """

    def __init__(self, parameter_set_name: ParameterSets, SOC_init_p: float, SOC_init_n: float, T: float):
        param_set = ParameterSets(name=parameter_set_name)
        df = electrode.Electrode.parse_csv(file_path=param_set.BATTERY_CELL_DIR)
        rho = df['Density [kg m^-3]']
        Vol = df['Volume [m^3]']
        C_p = df['Specific Heat [J K^-1 kg^-1]']
        h = df['Heat Transfer Coefficient [J s^-1 K^-1]']
        A = df['Surface Area [m^2]']
        cap = df['Capacity [A hr]']
        V_max = df['Maximum Potential Cut-off [V]']
        V_min = df['Minimum Potential Cut-off [V]']
        # initialize electrodes and electrolyte
        elec_p = electrode.PElectrode(file_path=param_set.POSITIVE_ELECTRODE_DIR,
                                      SOC_init=SOC_init_p, T=T, func_OCP=param_set.OCP_ref_p_,
                                      func_dOCPdT=param_set.dOCPdT_p_)
        elec_n = electrode.NElectrode(file_path=param_set.NEGATIVE_ELECTRODE_DIR,
                                      SOC_init=SOC_init_n, T=T, func_OCP=param_set.OCP_ref_n_,
                                      func_dOCPdT=param_set.dOCPdT_n_)
        electrolyte_ = electrolyte.Electrolyte(file_path=param_set.ELECTROLYTE_DIR)
        super().__init__(T_=T, rho=rho, Vol=Vol, C_p=C_p, h=h, A=A, cap=cap, V_max=V_max, V_min=V_min, elec_p=elec_p,
                         elec_n=elec_n, electrolyte=electrolyte_)

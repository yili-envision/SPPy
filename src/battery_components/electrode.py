import collections
import numpy as np
import pandas as pd

from src.calc_helpers import constants
from src.warnings_and_exceptions import custom_exceptions


class Electrode:
    """
    This class is used to create an electrode object. This object is used to store the electrode parameters and provide
    relevant electrode methods. It takes input parameters from the csv file. The electrode parameters are stored as
    attributes of the object.
    """
    def __init__(self, file_path, SOC_init, T, func_OCP, func_dOCPdT):
        """
        Electrode class constructor
        :param file_path: file path of the csv containing the electrode parameters.
        :param SOC_init: state of charge of the electrode and is between 0 and 1.
        :param T: current electrode temperature.
        :param func_OCP: function that describes the OCP of the electrode.
        :param func_dOCPdT: a function that describes the change of OCP with temperature
        """
        # Read and parse the csv file.
        df = Electrode.parse_csv(file_path=file_path)
        # Relevant instance variables are assigned.
        self.L = df['Electrode Thickness [m]']
        self.A = df['Electrode Area [m^2]']
        self.kappa = df['Ionic Conductivity [S m^-1]']
        self.epsilon = df['Volume Fraction']
        self.max_conc = df['Max. Conc. [mol m^-3]']
        self.R = df['Radius [m]']
        self.S = df['Electroactive Area [m^2]']
        if np.isnan(self.S):
            self.S = 3 * self.epsilon * (self.A * self.L) / self.R
        self.T_ref = df['Reference Temperature [K]']
        self.D_ref = df['Reference Diffusitivity [m^2 s^-1]']
        self.k_ref = df['Reference Rate Constant [m^2.5 mol^-0.5 s^-1]']
        self.Ea_D = df['Activation Energy of Diffusion [J mol^-1]']
        self.Ea_R = df['Activation Energy of Reaction [J mol^-1]']
        self.alpha = df['Anodic Transfer Coefficient']
        self.brugg = df['Bruggerman Coefficient']
        self.kappa_eff = self.kappa * (self.epsilon ** self.brugg)
        self.electrode_type = "none"
        # Set current SOC and temperature
        # Check if SOC is within the threshold
        if (SOC_init<=0) or (SOC_init>=1):
            raise custom_exceptions.InvalidSOCException(self.electrode_type)
        self.SOC_ = SOC_init
        self.T = T
        # set OCP and dOCPdT functions
        # Check if inputted func_OCP is a function type.
        if not isinstance(func_OCP, collections.abc.Callable):
            raise TypeError("func_OCP argument needs to be of a function type.")
        self.func_OCP = func_OCP
        # Check if inputted func_dOCPdt is a function type.
        if isinstance(func_dOCPdT, collections.abc.Callable):
            self.func_dOCPdT = func_dOCPdT
        else:
            raise TypeError("func_dOCPdT needs to be a None or Function type")

    @staticmethod
    def parse_csv(file_path):
        """
        reads the csv file and returns a Pandas DataFrame.
        :param file_path: the absolute or relative file drectory of the csv file.
        :return: the dataframe with the column containing numerical values only.
        """
        return pd.read_csv(file_path, index_col=0)["Value"]

    @property
    def SOC(self):
        return self.SOC_

    @SOC.setter
    def SOC(self, new_SOC):
        if (new_SOC <= 0) or (new_SOC >= 1):
            raise custom_exceptions.InvalidSOCException(self.electrode_type)
        self.SOC_ = new_SOC

    @property
    def D(self):
        return self.D_ref * np.exp(-1 * self.Ea_D / constants.Constants.R * (1 / self.T - 1 / self.T_ref))

    @property
    def k(self):
        return self.k_ref * np.exp(self.Ea_R / constants.Constants.R * (1 / self.T_ref - 1 / self.T))

    @property
    def dOCPdT(self):
        return self.func_dOCPdT(self.SOC)

    @property
    def OCP(self):
        return self.func_OCP(self.SOC) + self.dOCPdT * (self.T - self.T_ref)

    def i_0(self, c_e):
        return self.k * self.max_conc * (c_e ** 0.5) * ((1 - self.SOC)**0.5) * (self.SOC ** 0.5)


class PElectrode(Electrode):
    """
    This class is used to create a Positive electrode object. This object is used to store the electrode parameters and
    provide relevant electrode methods. It inherits from the Electrode class.
    """
    def __init__(self, file_path, SOC_init, T, func_OCP, func_dOCPdT=None):
        super().__init__(file_path=file_path, SOC_init=SOC_init, T=T, func_OCP=func_OCP, func_dOCPdT=func_dOCPdT)
        self.electrode_type = 'p'


class NElectrode(Electrode):
    """
    This class is used to create a Negative electrode object. This object is used to store the electrode parameters and
    provide relevant electrode methods. It inherits from the Electrode class.
    """
    def __init__(self, file_path, SOC_init, T, func_OCP, func_dOCPdT=None):
        super().__init__(file_path=file_path, SOC_init=SOC_init, T=T, func_OCP=func_OCP, func_dOCPdT=func_dOCPdT)
        self.electrode_type = 'n'

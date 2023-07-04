from typing import Optional
from dataclasses import dataclass, field
import collections

import numpy as np
import pandas as pd

from SPPy.calc_helpers import constants
from SPPy.warnings_and_exceptions import custom_exceptions


@dataclass
class Electrode_:
    """
    This class is used to create an electrode object. This object is used to store the electrode parameters and provide
    relevant electrode methods. It takes input parameters from the csv file. The electrode parameters are stored as
    attributes of the object.
    """
    L: float # Electrode Thickness [m]
    A: float # Electrode Area [m^2]
    kappa: float # Ionic Conductivity [S m^-1]
    epsilon: float # Volume Fraction
    max_conc: float # Max. Conc. [mol m^-3]
    R: float # Radius [m]
    S: Optional[float] # Electroactive Area [m2]
    T_ref: float # Reference Temperature [K]
    D_ref: float # Reference Diffusitivity [m2/s]
    k_ref: float # Reference Rate Constant [m2.5 / (mol0.5 s)
    Ea_D: float # Activation Energy of Diffusion [J / mol]
    Ea_R: float # Activation Energy of Reaction [J / mol]
    alpha: float # Anodic Transfer Coefficient
    brugg: float # Bruggerman Coefficient
    SOC_init: float # intial SOC
    func_OCP: collections.abc.Callable[[float], [float]] # electrode open-circuit potential function that takes SOC as
    # its arguments
    func_dOCPdT: collections.abc.Callable[[float], [float]] # the function that represents the change of open-curcuit
    # potential with SOC
    T: float # electrode temperature, K
    electrode_type: str = field(default='none')  # electrode type: none, 'p', or 'n'

    def __post_init__(self):
        """
        Electrode class constructor
        :param file_path: file path of the csv containing the electrode parameters. Please adhere to the csv format
        in the data/param_pos-electrode.csv or data/param_neg-electrode.csv file.
        :param SOC_init: state of charge of the electrode and is between 0 and 1.
        :param T: current electrode temperature.
        :param func_OCP: function that describes the OCP of the electrode.
        :param func_dOCPdT: a function that describes the change of OCP with temperature
        """
        if np.isnan(self.S):
            self.S = 3 * self.epsilon * (self.A * self.L) / self.R
        self.kappa_eff = self.kappa * (self.epsilon ** self.brugg)

        # Check if SOC is within the threshold
        if (self.SOC_init <= 0) or (self.SOC_init >= 1):
            raise custom_exceptions.InvalidSOCException(self.electrode_type)
        self.SOC_ = self.SOC_init

        # Check if inputted func_OCP is a function type.
        if not isinstance(self.func_OCP, collections.abc.Callable):
            raise TypeError("func_OCP argument needs to be of a function type.")
        # Check if inputted func_dOCPdt is a function type.
        if isinstance(self.func_dOCPdT, collections.abc.Callable):
            self.func_dOCPdT = self.func_dOCPdT
        else:
            raise TypeError("func_dOCPdT needs to be a None or Function type")

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


class Electrode(Electrode_):
    """
    Electrode inherits from Electrode, and it reads most of its class attributes from the csv file.
    """
    def __init__(self, file_path, SOC_init, T, func_OCP, func_dOCPdT):
        """
        Electrode class constructor
        :param file_path: file path of the csv containing the electrode parameters. Please adhere to the csv format
        in the data/param_pos-electrode.csv or data/param_neg-electrode.csv file.
        :param SOC_init: state of charge of the electrode and is between 0 and 1.
        :param T: current electrode temperature.
        :param func_OCP: function that describes the OCP of the electrode.
        :param func_dOCPdT: a function that describes the change of OCP with temperature
        """
        df = Electrode.parse_csv(file_path=file_path) # Read and parse the csv file.
        L = df['Electrode Thickness [m]']
        A = df['Electrode Area [m^2]']
        kappa = df['Ionic Conductivity [S m^-1]']
        epsilon = df['Volume Fraction']
        max_conc = df['Max. Conc. [mol m^-3]']
        R = df['Radius [m]']
        S = df['Electroactive Area [m^2]']
        T_ref = df['Reference Temperature [K]']
        D_ref = df['Reference Diffusitivity [m^2 s^-1]']
        k_ref = df['Reference Rate Constant [m^2.5 mol^-0.5 s^-1]']
        Ea_D = df['Activation Energy of Diffusion [J mol^-1]']
        Ea_R = df['Activation Energy of Reaction [J mol^-1]']
        alpha = df['Anodic Transfer Coefficient']
        brugg = df['Bruggerman Coefficient']

        super().__init__(L=L, A=A, kappa=kappa, epsilon=epsilon, max_conc=max_conc, R=R, S=S, T_ref=T_ref, D_ref=D_ref,
                         k_ref=k_ref, Ea_D=Ea_D, Ea_R=Ea_R, alpha=alpha, brugg=brugg, SOC_init=SOC_init,
                         func_OCP=func_OCP, func_dOCPdT=func_dOCPdT, T=T)

    @staticmethod
    def parse_csv(file_path):
        """
        reads the csv file and returns a Pandas DataFrame.
        :param file_path: the absolute or relative file drectory of the csv file.
        :return: the dataframe with the column containing numerical values only.
        """
        return pd.read_csv(file_path, index_col=0)["Value"]


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

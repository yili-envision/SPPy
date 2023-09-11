__author__ = 'Moin Ahmed'
__copywrite__ = 'Copywrite 2023 by Moin Ahmed. All rights are reserved.'
__status__ = 'deployed'


import numpy as np

from SPPy.calc_helpers.constants import Constants
from SPPy.warnings_and_exceptions.custom_exceptions import InvalidElectrodeType


class SPM:
    """
    This class contains the methods for calculating the molar lithium flux, cell terminal voltage according to the
    single particle model.
    """
    @classmethod
    def molar_flux_electrode(cls, I: float, S: float, electrode_type: str) -> float:
        """
        Calculates the model lithium-ion flux [mol/m2/s] into the electrodes.
        :param I: (float) Applied current [A]
        :param S: (float) electrode electrochemically active area [m2]
        :param electrode_type: (str) positive electrode ('p') or negative electrode ('n')
        :return: (float) molar flux [mol/m2/s]
        """
        if electrode_type == 'p':
            return I / (Constants.F * S)
        elif electrode_type == 'n':
            return -I / (Constants.F * S)
        else:
            raise InvalidElectrodeType

    @staticmethod
    def flux_to_current(molar_flux: float, S: float, electrode_type: str) -> float:
        """
        Converts molar flux [mol/m2/s] to current [A].
        :param molar_flux: molar lithium-ion flux [mol/m2/s]
        :param S: (float) electrode electrochemically active area [m2]
        :param electrode_type: (str) positive electrode ('p') or negative electrode ('n')
        :return: (float) current [A]
        """
        if electrode_type == 'p':
            return molar_flux * Constants.F * S
        elif electrode_type == 'n':
            return -molar_flux * Constants.F * S
        else:
            raise InvalidElectrodeType

    @staticmethod
    def m(I, k, S, c_max, SOC, c_e) -> float:
        return I / (Constants.F * k * S * c_max * (c_e ** 0.5) * ((1 - SOC) ** 0.5) * (SOC ** 0.5))

    @staticmethod
    def calc_cell_terminal_voltage(OCP_p, OCP_n, m_p, m_n, R_cell, T, I) -> float:
        V = OCP_p - OCP_n
        V += (2 * Constants.R * T / Constants.F) * np.log((np.sqrt(m_p ** 2 + 4) + m_p) / 2)
        V += (2 * Constants.R * T / Constants.F) * np.log((np.sqrt(m_n ** 2 + 4) + m_n) / 2)
        V += I * R_cell
        return V

    def __call__(self, OCP_p, OCP_n, R_cell,
                 k_p, S_p, c_smax_p, SOC_p,
                 k_n, S_n, c_smax_n, SOC_n,
                 c_e,
                 T, I_p_i, I_n_i) -> float:
        """
        Calculates the cell terminal voltage.
        :param OCP_p: Open-circuit potential of the positive electrode [V]
        :param OCP_n: Open-circuit potential of the negative electrode [V]
        :param R_cell: Battery cell ohmic resistance [ohms]
        :param k_p: positive electrode rate constant [m2 mol0.5 / s]
        :param S_p:  positive electrode electro-active area [mol/m2]
        :param c_smax_p: positive electrode max. lithium conc. [mol]
        :param SOC_p: positive electrode SOC
        :param k_n: negative electrode rate constant [m2 mol0.5 / s]
        :param S_n: negative electrode electrochemical active area [m2/mol]
        :param c_smax_n: negative electrode max. lithium conc. [mol]
        :param SOC_n: negative electrode SOC
        :param c_e: electrolyte conc. [mol]
        :param T: Battery cell temperature [K]
        :param I_p_i: positiive electrode intercalation applied current [A]
        :param I_n_i: negative electrode intercalation applied current [A]
        :return: Battery cell terminal voltage [V]
        """
        m_p = self.m(I=I_p_i, k=k_p, S=S_p, c_max=c_smax_p, SOC=SOC_p, c_e=c_e)
        m_n = self.m(I=I_n_i, k=k_n, S=S_n, c_max=c_smax_n, SOC=SOC_n, c_e=c_e)
        return self.calc_cell_terminal_voltage(OCP_p=OCP_p, OCP_n=OCP_n, m_p=m_p, m_n=m_n, R_cell=R_cell, T=T, I=I_p_i)


class SPMe:
    """
    This class contains the methods to calculate the molar ionic flux in the electrode regions and the cell terminal
    voltage as expressed in the SPMe model [1].

    Reference:
    [1] S. J. Moura, F. B. Argomedo, R. Klein, A. Mirtabatabaei and M. Krstic,
    "Battery State Estimation for a Single Particle Model With Electrolyte Dynamics,"
    in IEEE Transactions on Control Systems Technology, vol. 25, no. 2, pp. 453-468, March 2017,
    doi: 10.1109/TCST.2016.2571663.
    """
    @classmethod
    def volumetric_molar_fux(cls, I: float, S:float, electrode_type: str) -> float:
        return SPM.molar_flux_electrode(I=I, S=S, electrode_type=electrode_type)

    @classmethod
    def a_s(cls, epsilon: float, R: float) -> float:
        """
        Calculates the electrode's interfacial surface area [m2/m3]
        :param epsilon: active material volume fraction
        :param R: radius of the electrode particle
        :return: (float) electrode's interfacial surface area [m2/m3]
        """
        return 3 * epsilon / R

import numpy as np

from SPPy.calc_helpers.constants import Constants
from SPPy.warnings_and_exceptions.custom_exceptions import InvalidElectrodeType


class SPModel:
    """
    This class contains the methods for calculating the molar lithium flux, cell terminal voltage according to the
    single particle model.
    """
    @staticmethod
    def molar_flux_electrode(I: float, S: float, electrode_type: str):
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
    def flux_to_current(molar_flux: float, S: float, electrode_type: str):
        """
        Converts molar flux [mol/m2/s] to current [A].
        :param molar_flux: molar lithium-ion flux [mol/m2/s]
        :param S: (float) electrode electrochemically active area [m2]
        :param electrode_type: (str) positive electrode ('p') or negative electrode ('n')
        :return: current [A]
        """
        if electrode_type == 'p':
            return molar_flux * Constants.F * S
        elif electrode_type == 'n':
            return -molar_flux * Constants.F * S
        else:
            raise InvalidElectrodeType

    @staticmethod
    def m(I, k, S, c_max, SOC, c_e):
        return I / (Constants.F * k * S * c_max * (c_e ** 0.5) * ((1 - SOC) ** 0.5) * (SOC ** 0.5))

    @staticmethod
    def calc_cell_terminal_voltage(OCP_p, OCP_n, m_p, m_n, R_cell, T, I):
        V = OCP_p - OCP_n
        V += (2 * Constants.R * T / Constants.F) * np.log((np.sqrt(m_p ** 2 + 4) + m_p) / 2)
        V += (2 * Constants.R * T / Constants.F) * np.log((np.sqrt(m_n ** 2 + 4) + m_n) / 2)
        V += I * R_cell
        return V

    def __call__(self, OCP_p, OCP_n, R_cell,
                 k_p, S_p, c_smax_p, SOC_p,
                 k_n, S_n, c_smax_n, SOC_n,
                 c_e,
                 T, I_p_i, I_n_i):
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

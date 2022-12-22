import numpy as np

from src.calc_helpers.constants import Constants


class SPModel:
    def __init__(self, isothermal= False, degradation=False):
        # Check for incorrect input argument types.
        if not isinstance(isothermal, bool):
            raise TypeError("isothermal argument needs to be a bool type.")
        if not isinstance(degradation, bool):
            raise TypeError("degradation argument needs to be a bool type.")
        # Assign class attributes.
        self.isothermal = isothermal
        self.degradation = degradation

    @staticmethod
    def SOC(c, c_max):
        return c/c_max

    @staticmethod
    def j(I, S, electrode_type):
        if electrode_type == 'p':
            return I/(Constants.F * S)
        elif electrode_type == 'n':
            return -I/(Constants.F * S)
        else:
            raise ValueError("Invalid Electrode Type")

    # @staticmethod
    # def scaled_j(I, S, R, D, c_max, electrode_type):
    #     return SPModel.j(I=I, S=S, electrode_type=electrode_type) * R / (D * c_max)

    def m(self, I, k, S, c_max, SOC, c_e):
        return I/(Constants.F * k * S * c_max * (c_e ** 0.5) * ((1 - SOC) ** 0.5) * (SOC ** 0.5))

    @staticmethod
    def calc_term_V(p_OCP, n_OCP, m_p, m_n, R_cell, T, I):
        V = p_OCP - n_OCP
        V += (2 * Constants.R * T / Constants.F) * np.log((np.sqrt(m_p ** 2 + 4) + m_p) / 2)
        V += (2 * Constants.R * T / Constants.F) * np.log((np.sqrt(m_n ** 2 + 4) + m_n) / 2)
        V += I * R_cell
        return V

    @staticmethod
    def calc_cap(cap_prev, I, dt):
        return cap_prev + (1/3600) * np.abs(I) * dt
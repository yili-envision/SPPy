from typing import Union

import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt
import scipy.interpolate

import SPPy


class OCVData:
    def __init__(self, b_cell: SPPy.BatteryCell, sol_exp: SPPy.Solution,
                 SOC_n_min_init: float = 0, SOC_n_max_init: float = 0.815,
                 SOC_p_min_init: float = 0.39, SOC_p_max_init = 1):
        self.b_cell = b_cell
        self.exp_data = sol_exp
        self.SOC_n_min = SOC_n_min_init
        self.SOC_n_max = SOC_n_max_init
        self.SOC_p_min = SOC_p_min_init
        self.SOC_p_max = SOC_p_max_init

    def OCP_n(self, SOC_LIB: float):
        SOC_n = SOC_LIB * (self.SOC_n_max - self.SOC_n_min) + self.SOC_n_min
        return self.b_cell.elec_n.func_OCP(SOC_n)

    def OCP_p(self, SOC_LIB: float):
        SOC_p = SOC_LIB * (self.SOC_p_max - self.SOC_p_min) + self.SOC_p_min
        return np.flip(self.b_cell.elec_p.func_OCP(SOC_p))

    def OCV(self, SOC_LIB: Union[float, npt.ArrayLike]):
        OCP_p_ = self.OCP_p(SOC_LIB=SOC_LIB)
        OCP_n_ = self.OCP_n(SOC_LIB=SOC_LIB)
        return OCP_p_, OCP_n_, OCP_p_ - OCP_n_

    def mse(self, array_SOC_LIB: npt.ArrayLike = np.linspace(0, 1)):
        _,_,array_sim = self.OCV(array_SOC_LIB)
        return np.mean((self.exp_data.V - array_sim) ** 2)

    def plot(self, array_SOC_LIB: npt.ArrayLike = np.linspace(0, 1)):
        # func_OCV_exp = scipy.interpolate.interp1d(self.exp_data.cap, self.exp_data.V)
        # Plots
        fig = plt.figure()
        ax1 = fig.add_subplot(211)
        _,_,array_OCV_ = self.OCV(SOC_LIB=self.exp_data.cap_discharge)
        ax1.plot(self.exp_data.cap_discharge, array_OCV_, label='sim')
        ax1.plot(self.exp_data.cap_discharge, self.exp_data.V, label='OCV')
        ax1.plot(array_SOC_LIB, self.OCP_p(array_SOC_LIB), linestyle='--', label='$OCP_p$')
        ax1.plot(array_SOC_LIB, self.OCP_n(array_SOC_LIB), linestyle='--', label='$OCP_n$')

        ax2 = fig.add_subplot(212)
        ax2.plot(self.exp_data.cap_discharge, self.exp_data.V - array_OCV_,
                 label=f'{self.mse(array_SOC_LIB=self.exp_data.cap_discharge)}')
        ax2.set_ylabel('$\Delta$V')
        ax2.legend()

        ax1.legend()
        plt.show()

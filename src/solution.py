import numpy as np
import matplotlib.pyplot as plt

from src.calc_helpers.constants import Constants


class Solution:
    def __init__(self, t, I, V, x_surf_p, x_surf_n, cap, T, name=None):
        self.t = np.array(t[:len(V)])
        self.I = np.array(I[:len(V)])
        self.V = np.array(V)
        self.x_surf_p = np.array(x_surf_p)
        self.x_surf_n = np.array(x_surf_n)
        self.cap = np.array(cap)
        self.T = np.array(T)
        self.name = name

    def initiate_single_plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        return ax

    def single_plot(self, x_var, y_var, x_label, y_label):
        ax = self.initiate_single_plot()
        ax.plot(x_var, y_var)
        ax.set_xlabel(xlabel= x_label)
        ax.set_ylabel(ylabel=y_label)
        plt.show()
    def plot_tV(self):
        self.single_plot(self.t, self.V, x_label='t [s]', y_label='V [V]')

    def plot_capV(self):
        self.single_plot(self.cap, self.V, x_label= 'capacity [Ahr]', y_label='V [V]')

    def comprehensive_plot(self):
        num_rows = 3
        num_cols = 2
        fig = plt.figure(figsize=(6.4, 7.2))

        ax1 = fig.add_subplot(num_rows, num_cols, 1)
        ax1.plot(self.t, self.V)
        ax1.set_xlabel('Time [s]')
        ax1.set_ylabel('V [V]')
        ax1.set_title('V vs. Time')

        ax2 = fig.add_subplot(num_rows, num_cols, 2)
        ax2.plot(self.cap, self.V)
        ax2.set_xlabel('Capacity [Ahr]')
        ax2.set_ylabel('V [V]')
        ax2.set_title('V vs. Capacity')

        ax3 = fig.add_subplot(num_rows, num_cols, 3)
        ax3.plot(self.t, self.x_surf_p)
        ax3.set_xlabel('Time [s]')
        ax3.set_ylabel('SOC')
        ax3.set_title('Positive Electrode SOC')

        ax4 = fig.add_subplot(num_rows, num_cols, 4)
        ax4.plot(self.t, self.x_surf_n)
        ax4.set_xlabel('Time [s]')
        ax4.set_ylabel('SOC')
        ax4.set_title('Negative Electrode SOC')

        ax5 = fig.add_subplot(num_rows, num_cols, 5)
        ax5.plot(self.t, self.T - Constants.T_abs)
        ax5.set_xlabel('Time [s]')
        ax5.set_ylabel('Temperature [C]')
        ax5.set_title('Battery Cell Surface Temp.')

        ax6 = fig.add_subplot(num_rows, num_cols, 6)
        ax6.plot(self.cap, self.T - Constants.T_abs)
        ax6.set_xlabel('Capacity [Ahr]')
        ax6.set_ylabel('Temperature [C]')
        ax6.set_title('Battery Cell Surface Temp.')

        plt.tight_layout()
        plt.show()
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

from SPPy.calc_helpers.constants import Constants


class Solution:
    def __init__(self, cycle_num, cycle_step, t, I, V, x_surf_p, x_surf_n, cap, cap_charge, cap_discharge,
                 battery_cap, T, R_cell, js, name=None, save_csv_dir=None):
        self.cycle_num = np.array(cycle_num)
        self.cycle_step = np.array(cycle_step)
        self.t = np.array(t[:len(V)])
        self.I = np.array(I[:len(V)])
        self.V = np.array(V)
        self.x_surf_p = np.array(x_surf_p)
        self.x_surf_n = np.array(x_surf_n)
        self.cap = np.array(cap)
        self.cap_charge = cap_charge
        self.cap_discharge = cap_discharge
        self.battery_cap = battery_cap
        self.T = np.array(T)
        self.R_cell = np.array(R_cell)
        self.name = name
        self.total_cycles = len(np.unique(self.cycle_num))
        self.js = js
        if save_csv_dir is not None:
            self.save_csv_func(save_csv_dir)

    def create_df(self):
        df = pd.DataFrame({
            'Time [s]': self.t,
            'Cycle No': self.cycle_num,
            'Step Name': self.cycle_step,
            'I [A]': self.I,
            'SOC_p': self.x_surf_p,
            'SOC_n': self.x_surf_n,
            'V [V]': self.V,
            'Temp [K]': self.T,
            'capacity [Ahr]': self.cap,
            'Charge cap. [Ahr]': self.cap_charge,
            'Discharge cap. [Ahr]': self.cap_discharge,
            'R_cell [ohm]': self.R_cell,
            'Battery cap [Ahr]': self.battery_cap,
            'j_s [A/m2]': self.js
        })
        return df

    def save_csv_func(self, output_file_dir):
        df = self.create_df()
        if self.name is not None:
            df.to_csv(output_file_dir + self.name + '.csv')
        else:
            raise ValueError("Sol name not given.")

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

    def filter_cycle_nums(self):
        return np.unique(self.cycle_num)

    def filter_cap(self, cycle_no):
        """
        returns the discharge capacity of specified cycle no
        :param cycle_no: (int) cycle no.
        :return: returns the discharge capacity of specified cycle no
        """
        df = self.create_df()
        return df[(df['Cycle No'] == cycle_no) & (df['Step Name'] == 'discharge')]['Discharge cap. [Ahr]'].to_numpy()

    def filter_charge_cap(self, cycle_no):
        """
        returns the charge capacity of specified cycle no
        :param cycle_no: (int) cycle no.
        :return: returns the discharge capacity of specified cycle no
        """
        return [cap_ for i, cap_ in enumerate(self.cap) if ((self.cycle_num[i] == cycle_no) and
                                                                         (self.cycle_step[i] == 'charge'))]

    def filter_battery_cap(self, cycle_no):
        """
        Returns the battery cap at the end of the inputted cycle no.
        :param cycle_no: (int) cycle number
        :return: (double) battery cap found at the of the cycle num.
        """
        df = self.create_df()
        return df[(df['Cycle No'] == cycle_no)]['Battery cap [Ahr]'].to_numpy()[-1]

    def filter_V(self, cycle_no):
        """
        returns the potential during the discharge phase of the cycling
        :param cycle_no: (int) cycle no.
        :return: returns the discharge capacity of specified cycle no
        """
        return [V_ for i, V_ in enumerate(self.V) if ((self.cycle_num[i] == cycle_no) and
                                                                 (self.cycle_step[i] == 'discharge'))]

    def filter_T(self, cycle_no):
        """
        returns the temperature during the discharge phase of the cycling.
        :param cycle_no: (int) cycle no.
        :return: returns the temperature of the specified cycle no
        """
        return [T_ for i, T_ in enumerate(self.T) if ((self.cycle_num[i] == cycle_no) and
                                                      (self.cycle_step[i] == 'discharge'))]

    def filter_R_cell(self, cycle_no):
        return [R_cell_ for i, R_cell_ in enumerate(self.R_cell) if self.cycle_num[i] == cycle_no][-1]

    def calc_discharge_cap(self, cycle_no):
        return self.filter_cap(cycle_no=cycle_no)[-1]

    def calc_discharge_R_cell(self):
        """
        calulates the internal battery cell resistance after each cycle.
        :return:
        """
        all_cycle_no = np.unique(self.cycle_num)
        return np.array([self.filter_R_cell(all_cycle_no[i]) for i in range(self.total_cycles)])

    def calc_battery_cap_array(self):
        return np.array([self.filter_battery_cap(i) for i in self.filter_cycle_nums()])

    def plot_tV(self):
        num_rows = 1
        num_cols = 1
        fig = plt.figure()

        ax1 = fig.add_subplot(num_rows, num_cols, 1)
        ax1.plot(self.t, self.V)
        ax1.set_xlabel('Time [s]')
        ax1.set_ylabel('V [V]')
        ax1.set_title('V vs. Time')

        plt.show()

    def dis_cap_array(self):
        return np.array([self.calc_discharge_cap(cycle_no_) for cycle_no_ in np.unique(self.cycle_num)])

    def comprehensive_plot(self):
        mpl.rcParams['lines.linewidth'] = 3
        plt.rc('axes', titlesize=15)
        plt.rc('axes', labelsize=15)
        num_rows = 2
        num_cols = 3
        fig = plt.figure(figsize=(6.4*3, 10.8))

        ax1 = fig.add_subplot(num_rows, num_cols, 1)
        ax1.plot(self.t, self.V)
        ax1.set_xlabel('Time [s]')
        ax1.set_ylabel('V [V]')
        ax1.set_title('V vs. Time')

        ax2 = fig.add_subplot(num_rows, num_cols, 2)
        if len(np.unique(self.cycle_num)) == 1:
            ax2.plot(self.cap, self.V)
        else:
            # omit cycle 0
            first_cycle_no = np.unique(self.cycle_num)[1]
            last_cycle_no = np.unique(self.cycle_num)[-1]
            cap_list_first = self.filter_cap(first_cycle_no)
            cap_list_last = self.filter_cap(last_cycle_no)
            V_list_first = self.filter_V(first_cycle_no)
            V_list_last = self.filter_V(last_cycle_no)
            ax2.plot(cap_list_first, V_list_first, label = f"cycle {first_cycle_no}")
            ax2.plot(cap_list_last, V_list_last, label = f"cycle {last_cycle_no}")
        ax2.set_xlabel('Capacity [Ahr]')
        ax2.set_ylabel('V [V]')
        ax2.set_title('V vs. Capacity')
        ax2.legend()

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
        if len(np.unique(self.cycle_num)) == 1:
            ax6.plot(self.cap, self.T - Constants.T_abs)
        else:
            # omit cycle 0
            first_cycle_no = np.unique(self.cycle_num)[1]
            last_cycle_no = np.unique(self.cycle_num)[-1]
            cap_list_first = self.filter_cap(first_cycle_no)
            cap_list_last = self.filter_cap(last_cycle_no)
            T_list_first = self.filter_T(first_cycle_no)
            T_list_last = self.filter_T(last_cycle_no)
            ax6.plot(cap_list_first, np.array(T_list_first) - Constants.T_abs, label=f"cycle {first_cycle_no}")
            ax6.plot(cap_list_last, np.array(T_list_last) - Constants.T_abs, label=f"cycle {last_cycle_no}")
        ax6.set_xlabel('Capacity [Ahr]')
        ax6.set_ylabel('Temperature [C]')
        ax6.set_title('Battery Cell Surface Temp.')
        ax6.legend()

        # ax7 = fig.add_subplot(num_rows, num_cols, 7)
        # ax7.scatter(np.unique(self.cycle_num), self.dis_cap_array())
        # ax7.set_xlabel('Cycle No.')
        # ax7.set_ylabel('Discharge Capacity [A hr]')
        # ax7.set_title('Cycling Performance')

        # ax8 = fig.add_subplot(num_rows, num_cols, 8)
        # ax8.scatter(np.unique(self.cycle_num), self.calc_discharge_R_cell()*1e3)
        # ax8.set_xlabel('Cycle No.')
        # ax8.set_ylabel(r'Internal resistance [m$\Omega$]')
        # ax8.set_title('Cycling Performance')

        plt.tight_layout()
        plt.show()
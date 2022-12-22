import numpy as np
from tqdm import tqdm

from src.solvers import base
from src.warnings_and_exceptions.custom_exceptions import *
from src.solution import Solution


class FiniteDifferences(base.BaseSolver):
    def __init__(self, b_cell, b_model, **operating_conditions):
        super().__init__(b_cell=b_cell, b_model=b_model, **operating_conditions)

    def create_r_grid(self):
        return np.linspace(0, self.b_cell.elec_p.R, 20), np.linspace(0, self.b_cell.elec_n.R, 20)

    def create_c_initial_condition(self, len_rp, len_rn):
        c_p = self.b_cell.elec_p.SOC * self.b_cell.elec_p.max_conc * np.ones(len_rp)
        c_n = self.b_cell.elec_n.SOC * self.b_cell.elec_n.max_conc * np.ones(len_rn)
        return c_p, c_n

    def solve_c_s(self, c_kprev_r, c_k_rprev, c_k_rnext, c_k_r, D, r, dt, dr, r_plus, r_neg):
        r_mid_plus = r + (r - r_plus) / 2
        r_mid_neg = r - (r_neg - r) / 2
        first_inner_deriv = r_mid_plus ** 2 * (c_k_rnext - c_k_r) / dr
        second_inner_deriv = r_mid_neg ** 2 * (c_k_r - c_k_rprev) / dr
        return c_kprev_r + (D * dt / r ** 2) * ((first_inner_deriv - second_inner_deriv) / dr)

    def impose_BC(self, r_array, c_array, I, S, D, electrode_type):
        dr = r_array[-1] - r_array[-2]
        c_array[-1] = c_array[-2] - self.b_model.j(I=I, S=S, electrode_type=electrode_type) * dr / D
        c_array[0] = c_array[1]
        return r_array, c_array

    def solve_c_profile(self, r_array, c_array, electrode_type, I, dt):
        if electrode_type == 'p':
            D = self.b_cell.elec_p.D
            R = self.b_cell.elec_p.R
            S = self.b_cell.elec_p.S
        elif electrode_type == 'n':
            D = self.b_cell.elec_n.D
            R = self.b_cell.elec_n.R
            S = self.b_cell.elec_n.S
        else:
            raise InvalidElectrodeType
        # impose boundary conditions
        r_array, c_array = self.impose_BC(r_array=r_array, c_array=c_array, I=I, S=S, D=D,
                                          electrode_type=electrode_type)
        # solve for c_profile
        for r_iter in range(1, len(c_array) - 1):
            dr = r_array[r_iter] - r_array[r_iter - 1]
            c_array[r_iter] = self.solve_c_s(c_kprev_r=c_array[r_iter], c_k_rprev=c_array[r_iter - 1],
                                             c_k_rnext=c_array[r_iter + 1],
                                             c_k_r=c_array[r_iter],
                                             D=self.b_cell.elec_p.D,
                                             r=r_array[r_iter],
                                             dt=dt,
                                             dr=dr,
                                             r_plus=r_array[r_iter + 1],
                                             r_neg=r_array[r_iter - 1])
        return c_array

    @staticmethod
    def check_max_conc(c_array, c_max):
        for conc in c_array:
            if conc > c_max:
                raise MaxConcReached

    def solve(self, sol_name = None):
        # create array for solutions
        V_list, x_p_list, x_n_list = [self.calc_V(I=self.I[0])],[self.b_cell.elec_p.SOC], [self.b_cell.elec_n.SOC]
        cap_list = [0]
        T_list = [self.b_cell.T]
        # create grid
        r_p, r_n = self.create_r_grid()
        # initial_condition
        c_p, c_n = self.create_c_initial_condition(len(r_p), len(r_n))
        for t_iter in tqdm(range(1, len(self.t))):
            # define dt and I
            dt = self.t[t_iter] - self.t[t_iter - 1]
            I = self.I[t_iter]
            # solve for c_p profile
            c_p = self.solve_c_profile(r_array=r_p, c_array=c_p, electrode_type=self.b_cell.elec_p.electrode_type,
                                       I=I, dt=dt)
            FiniteDifferences.check_max_conc(c_array=c_p, c_max=self.b_cell.elec_p.max_conc)
            # solve for c_n profile
            c_n = self.solve_c_profile(r_array=r_n, c_array=c_n, electrode_type=self.b_cell.elec_n.electrode_type,
                                       I=I, dt=dt)
            FiniteDifferences.check_max_conc(c_array=c_n, c_max=self.b_cell.elec_n.max_conc)
            # calc SOC_surf and update cell SOC parameters
            SOC_p = self.b_model.SOC(c_p[-1], self.b_cell.elec_p.max_conc)
            SOC_n = self.b_model.SOC(c_n[-1], self.b_cell.elec_n.max_conc)
            x_n_list.append(SOC_n)
            # self.b_cell.elec_p.SOC = self.b_model.SOC(c=c_p[-1], c_max=self.b_cell.elec_p.max_conc)
            # self.b_cell.elec_n.SOC = self.b_model.SOC(c=c_n[-1], c_max=self.b_cell.elec_n.max_conc)
        #     # calc terminal V
        #     V = self.calc_V(I=I)
        #     # check if threshold potential is reached
        #     try:
        #         self.check_potential_limits(V)
        #     except PotientialThesholdReached:
        #         break
        #     except Exception as e:
        #         print(e)
        #     # Calc capacity
        #     cap = self.b_model.calc_cap(cap_prev=cap_list[-1], I=I, dt=dt)
        #     # Calc and update T
        #     if self.b_model.isothermal:
        #         T = self.b_cell.T
        #     # Update solution list
        #     self.update_lists(x_p_list=x_p_list, x_n_list=x_n_list, V_list=V_list, cap_list=cap_list, T_list=T_list,
        #              V=V, cap=cap, T=T)
        # return Solution(t=self.t, I=self.I, V=V_list, x_surf_p=x_p_list, x_surf_n=x_n_list, cap=cap_list, T=T_list,
        #                 name=sol_name)
        return c_n

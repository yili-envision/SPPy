import numpy as np
from scipy.optimize import bisect
from tqdm import tqdm

from SPPy.solvers.base import BaseSolver, timer
from SPPy.calc_helpers.constants import Constants
from SPPy.calc_helpers import ode_solvers
from SPPy.solution import Solution
from SPPy.warnings_and_exceptions.custom_warnings import *
from SPPy.warnings_and_exceptions.custom_exceptions import *
from SPPy.models.thermal import Lumped
from SPPy.cycler.base import BaseCycler
from SPPy.cycler.discharge import CustomDischarge


class EigenFuncExp(BaseSolver):
    """
    Mathematical Formulation Reference:
    1. Guo, M., Sikha, G., & White, R. E. (2011). Single-Particle Model for a Lithium-Ion Cell: Thermal Behavior.
    Journal of The Electrochemical Society, 158(2), A122. https://doi.org/10.1149/1.3521314/XML
    """
    def __init__(self, b_cell, b_model, N, **SEI_model):
        super().__init__(b_cell, b_model, **SEI_model)
        self.N = N

    @staticmethod
    def lambda_func(x):
        return np.sin(x) - x * np.cos(x)

    def lambda_bounds(self):
        return [(np.pi + np.pi * N_, 2 * np.pi + np.pi * N_) for N_ in range(self.N)]

    @property
    def lambda_roots(self):
        bounds = self.lambda_bounds()
        return [bisect(EigenFuncExp.lambda_func, bounds[N_][0], bounds[N_][1]) for N_ in range(self.N)]

    def scaled_j(self, I, R, S, D, c_s_max, electrode_type):
        if electrode_type == 'p':
            return -I*R / (Constants.F * S * D * c_s_max)
        elif electrode_type == 'n':
            return I*R / (Constants.F * S * D * c_s_max)

    @staticmethod
    def u_k_expression(lambda_k, D, R, scaled_flux):
        def u_k_odeFunc(x, t):
            return -(lambda_k ** 2) * D * x / (R ** 2) + 2 * D * scaled_flux / (R ** 2)
        return u_k_odeFunc

    def solve_u_k_j(self, root_value, t_prev, u_k_j_prev, scaled_j, dt, electrode_type):
        if electrode_type == 'p':
            u_k_p_func = EigenFuncExp.u_k_expression(lambda_k=root_value, D=self.b_cell.elec_p.D,
                                                     R=self.b_cell.elec_p.R, scaled_flux=scaled_j)
            return ode_solvers.rk4(func=u_k_p_func, t_prev=t_prev, y_prev=u_k_j_prev, step_size=dt)
        elif electrode_type == 'n':
            u_k_n_func = EigenFuncExp.u_k_expression(lambda_k=root_value, D=self.b_cell.elec_n.D,
                                                     R=self.b_cell.elec_n.R, scaled_flux=scaled_j)
            return ode_solvers.rk4(func=u_k_n_func, t_prev=t_prev, y_prev=u_k_j_prev, step_size=dt)
        else:
            raise InvalidElectrodeType

    def get_summation_term(self, t_prev, dt, u_k_p, u_k_n, scaled_j_p, scaled_j_n):
        sum_term_p = 0
        sum_term_n = 0
        # Solve for the summation term
        for iter_root, root_value in enumerate(self.lambda_roots):
            # sum term for the positive electrode
            u_k_p[iter_root] = self.solve_u_k_j(root_value=root_value, t_prev=t_prev, u_k_j_prev=u_k_p[iter_root],
                                                scaled_j=scaled_j_p, dt=dt,
                                                electrode_type=self.b_cell.elec_p.electrode_type)
            sum_term_p += u_k_p[iter_root] - (2 * scaled_j_p / (root_value ** 2))

            # sum term for the negative electrode
            u_k_n[iter_root] = self.solve_u_k_j(root_value=root_value, t_prev=t_prev, u_k_j_prev=u_k_n[iter_root],
                                                scaled_j=scaled_j_n, dt=dt,
                                                electrode_type=self.b_cell.elec_n.electrode_type)
            sum_term_n += u_k_n[iter_root] - (2 * scaled_j_n / (root_value ** 2))
        return u_k_p, u_k_n, sum_term_p, sum_term_n

    def calc_terminal_potential(self, I):
        m_p = self.b_model.m(I=I, k=self.b_cell.elec_p.k, S=self.b_cell.elec_p.S, c_e=self.b_cell.electrolyte.conc,
                             c_max=self.b_cell.elec_p.max_conc, SOC=self.b_cell.elec_p.SOC)
        m_n = self.b_model.m(I=I, k=self.b_cell.elec_n.k, S=self.b_cell.elec_n.S, c_e=self.b_cell.electrolyte.conc,
                             c_max=self.b_cell.elec_n.max_conc, SOC=self.b_cell.elec_n.SOC)
        V = self.b_model.calc_term_V(p_OCP=self.b_cell.elec_p.OCP,
                                     n_OCP=self.b_cell.elec_n.OCP,
                                     m_p=m_p, m_n=m_n, R_cell=self.b_cell.R_cell,
                                     T=self.b_cell.T, I=I)
        return V

    def calc_SOC_surf(self, scaled_j_p, scaled_j_n, u_k_p, u_k_n, integ_term_p, integ_term_n, x_p_init, x_n_init,
                      dt, t_prev):
        # Calculate and update the addition terms
        u_k_p, u_k_n, sum_term_p, sum_term_n = self.get_summation_term(t_prev, dt, u_k_p, u_k_n, scaled_j_p,
                                                                       scaled_j_n)
        # Update integration terms for both electrode
        integ_term_p += 3 * (self.b_cell.elec_p.D * scaled_j_p / (self.b_cell.elec_p.R ** 2)) * dt
        integ_term_n += 3 * (self.b_cell.elec_n.D * scaled_j_n / (self.b_cell.elec_n.R ** 2)) * dt
        # now solve for surface SOC for both electrodes
        self.b_cell.elec_p.SOC = x_p_init + scaled_j_p / 5 + integ_term_p + sum_term_p # positive electrode
        self.b_cell.elec_n.SOC = x_n_init + scaled_j_n / 5 + integ_term_n + sum_term_n # negative electrode
        return u_k_p, u_k_n, sum_term_p, sum_term_n, integ_term_p, integ_term_n

    @timer
    def solve(self, cycler, sol_name = None, save_csv_dir=None, verbose=False, t_increment=0.1,
              termination_criteria='V', adaptive_step=False):

        # check for input parameter types
        if not isinstance(cycler, BaseCycler):
            raise TypeError("cycler needs to be a Cycler object.")

        # initialize result storage lists
        x_p_list, x_n_list, V_list, cap_list, cap_charge_list, cap_discharge_list = [], [], [], [], [], []
        battery_cap_list = []
        t_list, I_list, T_list, R_cell_list, js_list = [], [], [], [], []
        cycle_list, step_name_list = [], []  # cycler specific information

        # initialize calculation parameters
        integ_term_p, integ_term_n = 0, 0 # integration terms
        u_k_p, u_k_n = np.zeros(self.N), np.zeros(self.N)
        x_p_init, x_n_init = self.b_cell.elec_p.SOC, self.b_cell.elec_n.SOC # initial surface SOC of electrodes

        t_model = Lumped(b_cell=self.b_cell) # thermal model object

        for cycle_no in tqdm(range(cycler.num_cycles)):
            for step in cycler.cycle_steps:
                cap = 0
                cap_charge = 0
                cap_discharge = 0
                t_prev =0
                step_completed = False
                while not step_completed:
                    if isinstance(cycler, CustomDischarge):
                        I = cycler.get_current(step, t_prev)
                    else:
                        I = cycler.get_current(step)
                    t_curr = t_prev + t_increment
                    dt = t_increment

                    # break condition for rest time
                    if ((step == "rest") and (t_curr > cycler.rest_time)):
                        step_completed = True

                    # Calc total electrode surface flux
                    scaled_j_p = self.scaled_j(I=I, R= self.b_cell.elec_p.R, S=self.b_cell.elec_p.S, D=self.b_cell.elec_p.D,
                                               c_s_max=self.b_cell.elec_p.max_conc, electrode_type='p')
                    scaled_j_n = self.scaled_j(I=I, R=self.b_cell.elec_n.R, S=self.b_cell.elec_n.S, D=self.b_cell.elec_n.D,
                                               c_s_max=self.b_cell.elec_n.max_conc, electrode_type='n')

                    # Account for SEI growth
                    if self.b_model.SEI_growth:
                        self.SEI_model.solve(I=I, dt=dt)
                        # self.b_cell.R_cell += self.SEI_model.resistance
                        self.b_cell.R_cell += self.SEI_model.delta_resistance(js_prev=self.SEI_model.j_s_prev, dt=dt)
                        self.b_cell.cap += self.SEI_model.delta_cap(self.b_cell.elec_n.S)
                        print(self.b_cell.cap)
                        scaled_j_n -= self.SEI_model.j_s_prev / Constants.F
                    # R_cell_list.append(self.b_cell.R_cell)

                    try:
                        u_k_p, u_k_n, sum_term_p, sum_term_n, integ_term_p, integ_term_n = \
                            self.calc_SOC_surf(scaled_j_p=scaled_j_p, scaled_j_n=scaled_j_n, u_k_p=u_k_p, u_k_n=u_k_n,
                                               integ_term_p=integ_term_p, integ_term_n=integ_term_n, x_p_init=x_p_init,
                                               x_n_init=x_n_init, dt=dt, t_prev=t_prev) # Calc the surface SOC
                    except InvalidSOCException as e:
                        print(e)
                        break

                    V = self.calc_terminal_potential(I=I) # calc battery cell terminal voltage
                    if V < self.b_cell.V_min:
                        threshold_potential_warning(V=V)
                        break

                    # Calc temp and update T_list if not isothermal
                    if not self.b_model.isothermal:
                        func_T = t_model.heat_balance(V=V, I=I)
                        self.b_cell.T = ode_solvers.rk4(func=func_T, t_prev=t_prev, y_prev=self.b_cell.T,
                                                        step_size=dt)

                    # Calc charge, discharge, LIB capacity
                    cap = self.b_model.calc_cap(cap_prev=cap, Q=self.b_cell.cap ,I=I, dt=dt)
                    delta_cap = self.b_model.delta_cap(Q=self.b_cell.cap,I=I, dt=dt)
                    if step == "charge":
                        cap_charge = self.b_model.calc_cap(cap_prev=cap_charge, Q=self.b_cell.cap, I=I, dt=dt)
                        cycler.SOC_LIB += delta_cap
                    elif step == "discharge":
                        cap_discharge = self.b_model.calc_cap(cap_prev=cap_discharge, Q=self.b_cell.cap, I=I, dt=dt)
                        cycler.SOC_LIB -= delta_cap

                    # break condition for charge and discharge if stop criteria is V-based
                    if termination_criteria == 'V':
                        if ((step == "charge") and (V > cycler.V_max)):
                            step_completed = True
                        if ((step == "discharge") and (V < cycler.V_min)):
                            step_completed = True
                    # break condition for charge and discharge if stop criteria is SOC-based
                    elif termination_criteria == 'SOC':
                        if ((step == "charge") and (cycler.SOC_LIB > cycler.SOC_max)):
                            step_completed = True
                        if ((step == "discharge") and (cycler.SOC_LIB < cycler.SOC_min)):
                            step_completed = True
                    # break condition for charge and discharge if stop criteria is time based
                    elif termination_criteria == 'time':
                        if step == "discharge" and cycler.time_elapsed > cycler.t_max:
                            step_completed = True

                    #update time
                    t_prev = t_curr
                    cycler.time_elapsed += t_increment

                    # Update results lists
                    t_list.append(cycler.time_elapsed)
                    cycle_list.append(cycle_no)
                    step_name_list.append(step)
                    I_list.append(I)
                    x_p_list.append(self.b_cell.elec_p.SOC)
                    x_n_list.append(self.b_cell.elec_n.SOC)
                    V_list.append(V)
                    T_list.append(self.b_cell.T)
                    cap_list.append(cap)
                    cap_charge_list.append(cap_charge)
                    cap_discharge_list.append(cap_discharge)
                    R_cell_list.append(self.b_cell.R_cell)
                    battery_cap_list.append(self.b_cell.cap)
                    if self.b_model.SEI_growth:
                        js_list.append(self.SEI_model.j_s_prev)
                    else:
                        js_list.append(0)

                    if verbose:
                        print("time elapsed [s]: ", cycler.time_elapsed, ", cycle_no: ", cycle_no,
                              'step: ', step, "current [A]", I,", terminal voltage [V]: ", V, ", SOC_LIB: ", cycler.SOC_LIB,
                              "cap: ", cap)

        return Solution(cycle_num=cycle_list, cycle_step=step_name_list, t=t_list, I=I_list, V=V_list,
                        x_surf_p=x_p_list, x_surf_n=x_n_list,
                        cap=cap_list, cap_charge=cap_charge_list, cap_discharge=cap_discharge_list,
                        battery_cap=battery_cap_list,
                        T=T_list, R_cell=R_cell_list, js=js_list,
                        name= sol_name, save_csv_dir=save_csv_dir)

    def simple_solve(self, cycler: CustomDischarge, verbose: bool = False):

        # check for input parameter types
        if not isinstance(cycler, CustomDischarge):
            raise TypeError("cycler needs to be a CustomDischarge cycler object.")

        # initialize result storage lists
        x_p_list, x_n_list, V_list, cap_list, cap_charge_list, cap_discharge_list = [], [], [], [], [], []
        battery_cap_list = []
        t_list, I_list, T_list, R_cell_list, js_list = [], [], [], [], []
        cycle_list, step_name_list = [], []  # cycler specific information

        # initialize calculation parameters
        integ_term_p, integ_term_n = 0, 0 # integration terms
        u_k_p, u_k_n = np.zeros(self.N), np.zeros(self.N)
        x_p_init, x_n_init = self.b_cell.elec_p.SOC, self.b_cell.elec_n.SOC # initial surface SOC of electrodes

        t_model = Lumped(b_cell=self.b_cell) # thermal model object

        cap = 0
        cap_charge = 0
        cap_discharge = 0
        t_prev =0
        step_completed = False
        for k in range(len(cycler.t_array)-1):
            t_curr = cycler.t_array[k]
            dt = cycler.t_array[k+1] - cycler.t_array[k]
            I = cycler.I_array[k]

            # Calc total electrode surface flux
            scaled_j_p = self.scaled_j(I=I, R= self.b_cell.elec_p.R, S=self.b_cell.elec_p.S, D=self.b_cell.elec_p.D,
                                       c_s_max=self.b_cell.elec_p.max_conc, electrode_type='p')
            scaled_j_n = self.scaled_j(I=I, R=self.b_cell.elec_n.R, S=self.b_cell.elec_n.S, D=self.b_cell.elec_n.D,
                                       c_s_max=self.b_cell.elec_n.max_conc, electrode_type='n')

            # Account for SEI growth
            if self.b_model.SEI_growth:
                self.SEI_model.solve(I=I, dt=dt)
                # self.b_cell.R_cell += self.SEI_model.resistance
                self.b_cell.R_cell += self.SEI_model.delta_resistance(js_prev=self.SEI_model.j_s_prev, dt=dt)
                self.b_cell.cap += self.SEI_model.delta_cap(self.b_cell.elec_n.S)
                print(self.b_cell.cap)
                scaled_j_n -= self.SEI_model.j_s_prev / Constants.F
            # R_cell_list.append(self.b_cell.R_cell)

            try:
                u_k_p, u_k_n, sum_term_p, sum_term_n, integ_term_p, integ_term_n = \
                    self.calc_SOC_surf(scaled_j_p=scaled_j_p, scaled_j_n=scaled_j_n, u_k_p=u_k_p, u_k_n=u_k_n,
                                       integ_term_p=integ_term_p, integ_term_n=integ_term_n, x_p_init=x_p_init,
                                       x_n_init=x_n_init, dt=dt, t_prev=t_prev) # Calc the surface SOC
            except InvalidSOCException as e:
                print(e)
                break

            V = self.calc_terminal_potential(I=I) # calc battery cell terminal voltage
            if V < self.b_cell.V_min:
                threshold_potential_warning(V=V)
                break

            # Calc temp and update T_list if not isothermal
            if not self.b_model.isothermal:
                func_T = t_model.heat_balance(V=V, I=I)
                self.b_cell.T = ode_solvers.rk4(func=func_T, t_prev=t_prev, y_prev=self.b_cell.T,
                                                step_size=dt)

            #update time
            t_prev = t_curr
            cycler.time_elapsed = cycler.t_array[k]

            # Update results lists
            t_list.append(cycler.time_elapsed)
            I_list.append(I)
            x_p_list.append(self.b_cell.elec_p.SOC)
            x_n_list.append(self.b_cell.elec_n.SOC)
            V_list.append(V)
            T_list.append(self.b_cell.T)
            cap_list.append(cap)
            cap_charge_list.append(cap_charge)
            cap_discharge_list.append(cap_discharge)
            R_cell_list.append(self.b_cell.R_cell)
            battery_cap_list.append(self.b_cell.cap)
            if self.b_model.SEI_growth:
                js_list.append(self.SEI_model.j_s_prev)
            else:
                js_list.append(0)

            if verbose:
                print("time elapsed [s]: ", cycler.time_elapsed, "current [A]", I,", terminal voltage [V]: ",
                      V, ", SOC_LIB: ", cycler.SOC_LIB, "cap: ", cap)

        return V_list

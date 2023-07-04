import numpy as np
from tqdm import tqdm

from SPPy.solvers.base import BaseSolver, timer
from SPPy.calc_helpers.constants import Constants
from SPPy.calc_helpers import ode_solvers
from SPPy.solution import Solution
from SPPy.warnings_and_exceptions.custom_warnings import *
from SPPy.warnings_and_exceptions.custom_exceptions import *
from SPPy.solvers.electrode_surf_conc import EigenFuncExp
from SPPy.models.thermal import Lumped
from SPPy.cycler.base import BaseCycler
from SPPy.cycler.discharge import CustomDischarge


class SPPySolver(BaseSolver):
    """
    This class contains the attributes and methods to solve for the cell terminal voltage, battery cell temperature,
    and SEI degradation during battery cycling. The cell terminal voltage is solved using the single particle (SP) model.
    It uses the Eigen Expansion Function method to solve for the electrode surface SOC.
    """
    def __init__(self, b_cell, b_model, N, **SEI_model):
        super().__init__(b_cell, b_model, **SEI_model)
        self.N = N

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
        SOC_solver_p = EigenFuncExp(x_init=self.b_cell.elec_p.SOC, n=self.N, electrode_type='p')
        SOC_solver_n = EigenFuncExp(x_init=self.b_cell.elec_n.SOC, n=self.N, electrode_type='n')

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

                    # # Account for SEI growth
                    # if self.b_model.SEI_growth:
                    #     self.SEI_model.solve(I=I, dt=dt)
                    #     # self.b_cell.R_cell += self.SEI_model.resistance
                    #     self.b_cell.R_cell += self.SEI_model.delta_resistance(js_prev=self.SEI_model.j_s_prev, dt=dt)
                    #     self.b_cell.cap += self.SEI_model.delta_cap(self.b_cell.elec_n.S)
                    #     print(self.b_cell.cap)
                    #     scaled_j_n -= self.SEI_model.j_s_prev / Constants.F
                    # # R_cell_list.append(self.b_cell.R_cell)

                    try:
                        self.b_cell.elec_p.SOC = SOC_solver_p(dt=dt, t_prev=t_prev, i_app=I,
                                                              R=self.b_cell.elec_p.R,
                                                              S=self.b_cell.elec_p.S,
                                                              D_s=self.b_cell.elec_p.D,
                                                              c_smax=self.b_cell.elec_p.max_conc)
                        self.b_cell.elec_n.SOC = SOC_solver_n(dt=dt, t_prev=t_prev, i_app=I,
                                                              R=self.b_cell.elec_n.R,
                                                              S=self.b_cell.elec_n.S,
                                                              D_s=self.b_cell.elec_n.D,
                                                              c_smax=self.b_cell.elec_n.max_conc)
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

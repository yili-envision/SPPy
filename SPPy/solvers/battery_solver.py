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
    and SEI degradation during battery cycling.
    The cell terminal voltage is solved using the single particle (SP) model. It uses the Eigen Expansion Function
    method to solve for the electrode surface SOC.
    The cell surface temperature is solved using the lumped cell thermal balance. The heat balance ODE is solved using
    the rk4 method.
    """

    def __init__(self, b_cell, isothermal: bool = True, degradation: bool = False, N: int = 5, **SEI_model):
        super().__init__(b_cell, **SEI_model)
        self.N = N
        # Check for incorrect input argument types.
        if not isinstance(isothermal, bool):
            raise TypeError("isothermal argument needs to be a bool type.")
        if not isinstance(degradation, bool):
            raise TypeError("degradation argument needs to be a bool type.")
        # Assign class attributes.
        self.bool_isothermal = isothermal
        self.bool_degradation = degradation

    def calc_terminal_potential(self, I):
        return self.b_model(OCP_p=self.b_cell.elec_p.OCP, OCP_n=self.b_cell.elec_n.OCP, R_cell=self.b_cell.R_cell,
                            k_p=self.b_cell.elec_p.k, S_p=self.b_cell.elec_p.S, c_smax_p=self.b_cell.elec_p.max_conc,
                            SOC_p=self.b_cell.elec_p.SOC,
                            k_n=self.b_cell.elec_n.k, S_n=self.b_cell.elec_n.S, c_smax_n=self.b_cell.elec_n.max_conc,
                            SOC_n=self.b_cell.elec_n.SOC,
                            c_e=self.b_cell.electrolyte.conc, T=self.b_cell.T, I=I)

    @staticmethod
    def calc_cell_temp(t_model, t_prev, dt, temp_prev, V, I):
        """
        Solves for the heat balance using the ODE rk4 solver.
        :param t_model: Thermal model class
        :param t_prev: time values at the previous time step [s]
        :param dt: time difference between the current and previous times [s]
        :param V: cell terminal voltage [V]
        :param temp_prev: previous cell temperature [K]
        :param I: applied current [A]
        :return: cell temperature values [K]
        """
        if not isinstance(t_model, Lumped):
            raise TypeError("t_model needs to be a Thermal Model")
        func_heat_balance = t_model.heat_balance(V=V, I=I)
        return ode_solvers.rk4(func=func_heat_balance, t_prev=t_prev, y_prev=temp_prev, step_size=dt)


    @staticmethod
    def delta_cap(Q, I, dt):
        return (1 / 3600) * (np.abs(I) * dt / Q)

    def calc_cap(self, cap_prev, Q, I, dt):
        return cap_prev + self.delta_cap(Q=Q, I=I, dt=dt)

    @timer
    def solve(self, cycler, sol_name=None, save_csv_dir=None, verbose=False, t_increment=0.1,
              termination_criteria='V'):

        # check for input parameter types below.
        if not isinstance(cycler, BaseCycler):
            raise TypeError("cycler needs to be a Cycler object.")

        # initialize result storage lists below.
        x_p_list, x_n_list, V_list, cap_list, cap_charge_list, cap_discharge_list = [], [], [], [], [], []
        battery_cap_list = []
        t_list, I_list, T_list, R_cell_list, js_list = [], [], [], [], []
        cycle_list, step_name_list = [], []  # cycler specific information

        # initialize electrode surface SOC and temperature solvers instances below.
        SOC_solver_p = EigenFuncExp(x_init=self.b_cell.elec_p.SOC, n=self.N, electrode_type='p')
        SOC_solver_n = EigenFuncExp(x_init=self.b_cell.elec_n.SOC, n=self.N, electrode_type='n')

        t_model = Lumped(b_cell=self.b_cell)  # thermal model object

        # cycling simulation below. The first two loops iterate over the cycle numbers and cycling steps,
        # respectively. The following while loops checks for termination conditions and breaks when it reaches it.
        # The termination criteria are specified within the cycler instance.
        for cycle_no in tqdm(range(cycler.num_cycles)):
            for step in cycler.cycle_steps:
                cap = 0
                cap_charge = 0
                cap_discharge = 0
                t_prev = 0
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
                                                              c_smax=self.b_cell.elec_p.max_conc)  # calc p surf SOC
                        self.b_cell.elec_n.SOC = SOC_solver_n(dt=dt, t_prev=t_prev, i_app=I,
                                                              R=self.b_cell.elec_n.R,
                                                              S=self.b_cell.elec_n.S,
                                                              D_s=self.b_cell.elec_n.D,
                                                              c_smax=self.b_cell.elec_n.max_conc)  # calc n surf SOC
                    except InvalidSOCException as e:
                        print(e)
                        break

                    V = self.calc_terminal_potential(I=I)  # calc battery cell terminal voltage
                    if V < self.b_cell.V_min:
                        threshold_potential_warning(V=V)
                        break

                    # Calc temp and update T_list if not isothermal
                    if not self.bool_isothermal:
                        self.b_cell.T = self.calc_cell_temp(t_model=t_model, t_prev=t_prev, dt=dt,
                                                            temp_prev=self.b_cell.T, V=V, I=I)

                    # Calc charge capacity, discharge capacity, and overall LIB capacity
                    cap = self.calc_cap(cap_prev=cap, Q=self.b_cell.cap, I=I, dt=dt)
                    delta_cap = self.delta_cap(Q=self.b_cell.cap, I=I, dt=dt)
                    if step == "charge":
                        cap_charge = self.calc_cap(cap_prev=cap_charge, Q=self.b_cell.cap, I=I, dt=dt)
                        cycler.SOC_LIB += delta_cap
                    elif step == "discharge":
                        cap_discharge = self.calc_cap(cap_prev=cap_discharge, Q=self.b_cell.cap, I=I, dt=dt)
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

                    # update time
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
                    if self.bool_degradation:
                        js_list.append(self.SEI_model.j_s_prev)
                    else:
                        js_list.append(0)

                    if verbose:
                        print("time elapsed [s]: ", cycler.time_elapsed, ", cycle_no: ", cycle_no,
                              'step: ', step, "current [A]", I, ", terminal voltage [V]: ", V, ", SOC_LIB: ",
                              cycler.SOC_LIB,
                              "cap: ", cap)

        return Solution(cycle_num=cycle_list, cycle_step=step_name_list, t=t_list, I=I_list, V=V_list,
                        x_surf_p=x_p_list, x_surf_n=x_n_list,
                        cap=cap_list, cap_charge=cap_charge_list, cap_discharge=cap_discharge_list,
                        battery_cap=battery_cap_list,
                        T=T_list, R_cell=R_cell_list, js=js_list,
                        name=sol_name, save_csv_dir=save_csv_dir)

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
        integ_term_p, integ_term_n = 0, 0  # integration terms
        u_k_p, u_k_n = np.zeros(self.N), np.zeros(self.N)
        x_p_init, x_n_init = self.b_cell.elec_p.SOC, self.b_cell.elec_n.SOC  # initial surface SOC of electrodes

        t_model = Lumped(b_cell=self.b_cell)  # thermal model object

        cap = 0
        cap_charge = 0
        cap_discharge = 0
        t_prev = 0
        step_completed = False
        for k in range(len(cycler.t_array) - 1):
            t_curr = cycler.t_array[k]
            dt = cycler.t_array[k + 1] - cycler.t_array[k]
            I = cycler.I_array[k]

            # Calc total electrode surface flux
            scaled_j_p = self.scaled_j(I=I, R=self.b_cell.elec_p.R, S=self.b_cell.elec_p.S, D=self.b_cell.elec_p.D,
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
                                       x_n_init=x_n_init, dt=dt, t_prev=t_prev)  # Calc the surface SOC
            except InvalidSOCException as e:
                print(e)
                break

            V = self.calc_terminal_potential(I=I)  # calc battery cell terminal voltage
            if V < self.b_cell.V_min:
                threshold_potential_warning(V=V)
                break

            # Calc temp and update T_list if not isothermal
            if not self.b_model.isothermal:
                func_T = t_model.heat_balance(V=V, I=I)
                self.b_cell.T = ode_solvers.rk4(func=func_T, t_prev=t_prev, y_prev=self.b_cell.T,
                                                step_size=dt)

            # update time
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
                print("time elapsed [s]: ", cycler.time_elapsed, "current [A]", I, ", terminal voltage [V]: ",
                      V, ", SOC_LIB: ", cycler.SOC_LIB, "cap: ", cap)

        return V_list

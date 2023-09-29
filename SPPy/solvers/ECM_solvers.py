__author__ = 'Moin Ahmed'
__copywrite__ = 'Copywrite 2023 by Moin Ahmed. All rights are reserved.'
__status__ = 'deployed'

import tqdm

from SPPy.solvers.base import timer
from SPPy.battery_components.battery_cell import ECMBatteryCell
from SPPy.models.ECM import Thevenin1RC
from SPPy.cycler.base import BaseCycler
from SPPy.cycler.custom import CustomCycler
from SPPy.solvers.thermal_solvers import calc_cell_temp
from SPPy.sol_and_visualization.solution import ECMSolution


class BaseSolver:
    def __init__(self, battery_cell_instance: ECMBatteryCell, isothermal: bool):
        if isinstance(battery_cell_instance, ECMBatteryCell):
            self.b_cell = battery_cell_instance
        else:
            raise TypeError("ECM_obj must be an instance of Thevenin1RC class.")

        if isinstance(isothermal, bool):
            self.isothermal = isothermal
        else:
            raise TypeError("isothermal must be a boolean (True or False).")

        self.b_model = Thevenin1RC()


class DTSolver(BaseSolver):
    """
    This is the class that solves the ECM model equations for time and applied current arrays. It outputs the terminal
    SOC and voltage at the time steps specified by the input time array.

    The discrete time model for first-order Thevenin model is given by:

    z[k+1] = z[k] - delta_t*eta[k]*i_app[k]/capacity
    i_R1[k+1] = exp(-delta_t/(R1*C1))*i_R1[k] + (1-exp(-delta_t/(R1*C1))) * i_app[k]
    v[k] = OCV(z[k]) - R1*i_R1[k] - R0*i_app[k]

    Where k represents the time-point and delta_t represents the time-step between z[k+1] and z[k].
    """

    def __init__(self, battery_cell_instance: ECMBatteryCell, isothermal: bool):
        """
        The class constructor for the solver object.
        :params ECM_obj: (Thevenin1RC) ECM model object
        :params isothermal: (bool)
        :params t_app: (Numpy array) array of time.
        :params i_app: (Numpy array) array of applied battery current associated with the time array.
        :param v_exp: (Numpy array) array of experimental battery terminal voltage data.
        """
        super().__init__(battery_cell_instance=battery_cell_instance, isothermal=isothermal)

    def __calc_v(self, dt: float, i_app: float, i_r1_prev: float) -> tuple[float, float]:
        """
        Calculates the cell terminal voltage by first calculating the current across the R-C pair
        :param dt:
        :param i_app:
        :param i_r1_prev:
        :return:
        """
        i_r1_prev = Thevenin1RC.i_R1_next(dt=dt, i_app=i_app, i_R1_prev=i_r1_prev,
                                          R1=self.b_cell.R1, C1=self.b_cell.C1)
        v = Thevenin1RC.v(i_app=i_app, OCV=self.b_cell.func_ocv(self.b_cell.soc),
                          R0=self.b_cell.R0, R1=self.b_cell.R1, i_R1=i_r1_prev)
        return i_r1_prev, v

    def __solve_custom_step(self, cycling_step: CustomCycler, dt: float, verbose: bool):
        sol = ECMSolution()  # initialize the solution object
        sol.update(t=0.0, i_app=0.0, v=self.b_cell.ocv, temp=self.b_cell.temp, soc=self.b_cell.soc)

        t_prev = 0.0  # [s]
        i_r1_prev = 0.0  # [A]
        step_completed = False

        while not step_completed:
            t_curr = t_prev + dt
            i_app_prev = cycling_step.get_current(step_name='custom', t=t_prev)
            i_app_curr = cycling_step.get_current(step_name='custom', t=t_curr)

            # Calculate the SOC (and update the battery cell attribute), i_R1 [A], and v[V] for the current time step
            self.b_cell.soc = Thevenin1RC.soc_next(dt=dt, i_app=i_app_prev, SOC_prev=self.b_cell.soc,
                                                   Q=self.b_cell.cap,
                                                   eta=self.b_cell.eta)
            i_r1_prev, v = self.__calc_v(dt=dt, i_app=i_app_curr, i_r1_prev=i_r1_prev)

            # Calc temp
            if self.isothermal is not True:
                self.b_cell.temp = calc_cell_temp(t_prev=t_prev, dt=dt, temp_prev=self.b_cell.temp, V=v,
                                                  I=i_app_curr,
                                                  rho=self.b_cell.rho, Vol=self.b_cell.vol, C_p=self.b_cell.c_p,
                                                  OCV=self.b_cell.ocv, dOCVdT=self.b_cell.docpdtemp,
                                                  h=self.b_cell.h,
                                                  A=self.b_cell.area, T_amb=self.b_cell.temp_init)

            # loop termination criteria
            if v > cycling_step.V_max:
                step_completed = True
            if v < cycling_step.V_min:
                step_completed = True
            if t_curr > cycling_step.t_max:
                step_completed = True

            # update the sol object
            sol.update(t=t_curr, i_app=i_app_curr, v=v, temp=self.b_cell.temp, soc=self.b_cell.soc)
            t_prev = t_curr

            if verbose == True:
                print('t=', t_curr, ' i_app=', i_app_curr, ' v=', v, ' temp=', self.b_cell.temp, ' soc=', self.b_cell.soc)

        return sol

    def __solve_standard_cycling_step(self, cycler: BaseCycler, dt: float) -> ECMSolution:
        sol = ECMSolution()
        # update the initial values of sol object below
        sol.update(t=0.0, i_app=0.0, v=self.b_cell.ocv, temp=self.b_cell.temp, soc=self.b_cell.soc)
        for cycle_no in tqdm.tqdm(range(cycler.num_cycles)):
            for step in cycler.cycle_steps:
                t_prev = 0
                i_r1_prev = 0
                step_completed = False
                while not step_completed:
                    t_curr = t_prev + dt
                    i_app = -cycler.get_current(step=step)

                    # break condition for rest time
                    if step == "rest" and t_curr > cycler.rest_time:
                        step_completed = True

                    # calc. the SOC and i_R1 for the current time step
                    self.b_cell.soc = self.b_model.soc_next(dt=dt, i_app=i_app, SOC_prev=self.b_cell.soc,
                                                            Q=self.b_cell.cap, eta=self.b_cell.eta)
                    i_r1_prev, v = self.__calc_v(dt=dt, i_app=i_app, i_r1_prev=i_r1_prev)

                    # Calc temp
                    if self.isothermal is not True:
                        self.b_cell.temp = calc_cell_temp(t_prev=t_prev, dt=dt, temp_prev=self.b_cell.temp, V=v,
                                                          I=-i_app,
                                                          rho=self.b_cell.rho, Vol=self.b_cell.vol, C_p=self.b_cell.c_p,
                                                          OCV=self.b_cell.ocv, dOCVdT=self.b_cell.docpdtemp,
                                                          h=self.b_cell.h,
                                                          A=self.b_cell.area, T_amb=self.b_cell.temp_init)

                    # loop termination criteria
                    if ((step == "charge") and (v > cycler.V_max)):
                        step_completed = True
                    if ((step == "discharge") and (v < cycler.V_min)):
                        step_completed = True

                    # Below updates the simulation parameters for the next iteration
                    t_prev = t_curr

                    # update solution object
                    sol.update(t=t_curr, i_app=i_app, v=v, temp=self.b_cell.temp, soc=self.b_cell.soc)
        return sol

    @timer
    def solve(self, cycling_step: BaseCycler, dt: float = 0.1, verbose: bool = False) -> ECMSolution:
        if isinstance(cycling_step, CustomCycler):
            return self.__solve_custom_step(cycling_step=cycling_step, dt=dt, verbose=verbose)
        else:
            return self.__solve_standard_cycling_step(cycler=cycling_step, dt=dt)

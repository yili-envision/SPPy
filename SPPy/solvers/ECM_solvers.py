import numpy as np
import numpy.typing as npt
import tqdm

from SPPy.solvers.base import timer
from SPPy.battery_components.battery_cell import ECMBatteryCell
from SPPy.models.ECM import Thevenin1RC
from SPPy.cycler.base import BaseCycler
from SPPy.solvers.thermal_solvers import calc_cell_temp
from SPPy.solution import ECMSolutionInitializer, ECMSolution


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

    @timer
    def solve(self, cycler: BaseCycler, dt: float = 0.1):
        sol = ECMSolutionInitializer()
        # list for storing SOC and voltage values
        lst_t = [0]
        lst_v = [self.b_cell.OCV]  # solution storage list and stores the initial cell terminal value
        lst_T = [self.b_cell.T]
        for cycle_no in tqdm.tqdm(range(cycler.num_cycles)):
            for step in cycler.cycle_steps:
                t_prev = 0
                i_R1_prev=0
                step_completed = False
                while not step_completed:
                    t_curr = t_prev + dt
                    I = -cycler.get_current(step=step)

                    # break condition for rest time
                    if step == "rest" and t_curr > cycler.rest_time:
                        step_completed = True

                    # calc. the SOC and i_R1 for the current time step
                    self.b_cell.SOC = self.b_model.SOC_next(dt=dt, i_app=I, SOC_prev=self.b_cell.SOC,
                                                            Q=self.b_cell.cap, eta=self.b_cell.eta)
                    i_R1 = self.b_model.i_R1_next(dt=dt, i_app=I, i_R1_prev=i_R1_prev,
                                                       R1=self.b_cell.R1, C1=self.b_cell.C1)
                    # Calculate V
                    V = self.b_model.V(i_app=I, OCV=self.b_cell.OCV, R0=self.b_cell.R0, R1=self.b_cell.R1,
                                                i_R1=i_R1)
                    lst_v.append(V)
                    lst_t.append(t_curr)

                    # Calc temp
                    if self.isothermal is not True:
                        self.b_cell.T = calc_cell_temp(t_prev=t_prev, dt=dt, temp_prev=self.b_cell.T, V=V, I=-I,
                                                       rho=self.b_cell.rho, Vol=self.b_cell.Vol, C_p=self.b_cell.C_p,
                                                       OCV=self.b_cell.OCV, dOCVdT=self.b_cell.dOCPdT, h=self.b_cell.h,
                                                       A=self.b_cell.A, T_amb=self.b_cell.T_init)
                    lst_T.append(self.b_cell.T)

                    # loop termination criteria
                    if ((step == "charge") and (V > cycler.V_max)):
                        step_completed = True
                    if ((step == "discharge") and (V < cycler.V_min)):
                        step_completed = True

                    # Below updates the simulation parameters for the next iteration
                    i_R1_prev = i_R1
                    t_prev = t_curr

                    # update solution object
                    sol.update(t=t_curr, V=V, T=self.b_cell.T, I=I)
        return ECMSolution(sol)

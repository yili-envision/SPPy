from SPPy.battery_components.battery_cell import BatteryCell
from SPPy.models.single_particle_model import SPModel
from SPPy.warnings_and_exceptions.custom_exceptions import *
from SPPy.warnings_and_exceptions.custom_warnings import *
from SPPy.models.degradation import ROM_SEI
import time


class BaseSolver:
    def __init__(self, b_cell, **SEI_model):
        # Below checks and initializes the battery cell instance
        if not isinstance(b_cell, BatteryCell):
            raise TypeError('b_cell needs to be a BatteryCell object.')
        else:
            self.b_cell = b_cell

        self.b_model = SPModel()  # initializes the single particle model instance.
        # if self.b_model.SEI_growth:
        #     present = False
        #     for kwargs_ in SEI_model.keys():
        #         if kwargs_ == 'SEI_model':
        #             present = True
        #             break
        #     if present == False:
        #         raise ValueError("Need to provide SEI_model.")
        #     if not isinstance(SEI_model['SEI_model'], ROM_SEI):
        #         raise TypeError('SEI_model needs to be of ROM_SEI type.')
        #     else:
        #         self.SEI_model = SEI_model['SEI_model']

    def check_potential_limits(self, V):
        if V < self.b_cell.V_min:
            raise PotientialThesholdReached

    def update_lists(self, x_p_list, x_n_list, V_list, cap_list, T_list,
                     V, cap, T):
        # Check for input arguments
        if not isinstance(x_p_list, list):
            raise TypeError("x_p_list needs to be a list type.")
        if not isinstance(x_n_list, list):
            raise TypeError("x_n_list needs to be a list type.")
        if not isinstance(V_list, list):
            raise TypeError("V_list needs to be list type.")
        if not isinstance(cap_list, list):
            raise TypeError("cap_list needs to be a list type.")
        if not isinstance(T_list, list):
            raise TypeError("T_list needs to be T type")
        x_p_list.append(self.b_cell.elec_p.SOC)
        x_n_list.append(self.b_cell.elec_n.SOC)
        V_list.append(V)
        cap_list.append(cap)
        T_list.append(T)


def timer(solver_func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        sol = solver_func(*args, **kwargs)
        print(f"Solver execution time: {time.time() - start_time}s")
        return sol
    return wrapper
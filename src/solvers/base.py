from src.battery_components.battery_cell import BatteryCell
from src.models.single_particle_model import SPModel
from src.warnings_and_exceptions.custom_exceptions import *
from src.warnings_and_exceptions.custom_warnings import *
# from models.degradation import ROM_SEI
import time


class BaseSolver:
    def __init__(self, b_cell, b_model, **operating_conditions):
        # Check if the input arguments of the correct types.
        if not isinstance(b_cell, BatteryCell):
            raise TypeError('b_cell needs to be a BatteryCell object.')
        if not isinstance(b_model, SPModel):
            raise TypeError('b_model needs to be a SPModel object')
        # Ensure time and current arrays are present in the keywords input.
        t_present, I_present = False, False
        for index, key in enumerate(operating_conditions):
            if key == 't':
                t_present = True
            elif key == 'I':
                I_present = True
        if (t_present == False) or (I_present == False):
            raise InsufficientInputOperatingConditions
        # Assign class attributes.
        self.b_cell = b_cell
        self.b_model = b_model
        self.t = operating_conditions['t']
        self.I = operating_conditions['I']
        # if self.b_model.SEI_growth:
        #     present = False
        #     for kwargs_ in operating_conditions.keys():
        #         if kwargs_ == 'SEI_model':
        #             present = True
        #             break
        #     if present == False:
        #         raise ValueError("Need to provide SEI_model.")
        #     if not isinstance(operating_conditions['SEI_model'], ROM_SEI):
        #         raise TypeError('SEI_model needs to be of ROM_SEI type.')
        #     else:
        #         self.SEI_model = operating_conditions['SEI_model']

    def calc_V(self, I):
        m_p = self.b_model.m(I=I, k=self.b_cell.elec_p.k, S=self.b_cell.elec_p.S, c_e=self.b_cell.electrolyte.conc,
                             c_max=self.b_cell.elec_p.max_conc, SOC=self.b_cell.elec_p.SOC)
        m_n = self.b_model.m(I=I, k=self.b_cell.elec_n.k, S=self.b_cell.elec_n.S, c_e=self.b_cell.electrolyte.conc,
                             c_max=self.b_cell.elec_n.max_conc, SOC=self.b_cell.elec_n.SOC)
        V = self.b_model.calc_term_V(p_OCP=self.b_cell.elec_p.OCP,
                                     n_OCP=self.b_cell.elec_n.OCP,
                                     m_p=m_p, m_n=m_n, R_cell=self.b_cell.R_cell,
                                     T=self.b_cell.T, I=I)
        return V

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
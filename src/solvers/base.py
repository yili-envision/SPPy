from src.battery_components.battery_cell import BatteryCell
from src.models.single_particle_model import SPModel
from src.warnings_and_exceptions.custom_exceptions import *
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


def timer(solver_func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        sol = solver_func(*args, **kwargs)
        print(f"Solver execution time: {time.time() - start_time}s")
        return sol
    return wrapper
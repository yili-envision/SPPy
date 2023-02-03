import numpy as np

from src.battery_components.battery_cell import BatteryCell
from src.battery_components.electrode import Electrode
from src.calc_helpers.constants import Constants
from src.models.single_particle_model import SPModel


class ROM_SEI:
    """
    Literature Reference:
    1. Randell et al. "Controls oriented reduced order modeling of solid-electrolyte interphase layer growth". 2012.
    Journal of Power Sources. Vol: 209. pgs: 282-288.
    2. Elvira et al. JPS. 2021
    """
    def __init__(self, bCell, file_path, resistance_init):
        if not isinstance(bCell, BatteryCell):
            raise TypeError("bCell variable needs to be a Battery Cell object.")
        self.b_cell = bCell
        csv_file = Electrode.parse_csv(file_path=file_path)
        self.U_ref = csv_file['Side Reaction Reference Overpotential [V]'] # reaction potential
        self.i_0s = csv_file['Side Reaction Exchange Current [A m^2]']
        self.kappa = csv_file['Conductivity [S m^-1]'] # SEI film conductivity in Sm^-1.
        self.M_W = csv_file['Molar Weight [kg mol^-1]'] # Average SEI Molecular Weight
        self.rho = csv_file['Density [kg m^-3]'] # Average SEI Density
        self.resistance = resistance_init
        self.j_s_prev = None

    def j_tot(self, I):
        return SPModel.scaled_j(I=I, S=self.b_cell.elec_n.S, D=self.b_cell.elec_n.D, c_max=self.b_cell.elec_n.max_conc,
                                R=self.b_cell.elec_n.R, electrode_type='n')

    def eta_n(self, j_i_value):
        return (2 * Constants.R * self.b_cell.T / Constants.F) * (np.arcsinh(j_i_value /
                                                                             (2 * self.b_cell.elec_n.i_0(self.b_cell.electrolyte.conc))))

    def eta_s(self, j_i_value):
        return self.eta_n(j_i_value) + self.U_ref - self.b_cell.elec_n.OCP

    def j_s(self, j_i_value):
        return -self.i_0s * np.exp(-Constants.F * self.eta_s(j_i_value) / (2 * Constants.R * self.b_cell.T))

    def j_i(self, I, j_s):
        return self.j_tot(I) - j_s

    def solve_j_s(self, I, iter_no = 10):
        j_s_val = 0
        for i_ in range(iter_no):
            j_i_val = self.j_i(I, j_s_val)
            j_s_val = self.j_s(j_i_val)
        return j_s_val

    def delta_thickness(self, js_prev, dt):
        return -self.M_W * dt * js_prev / (self.rho * Constants.F)

    def delta_resistance(self, js_prev, dt):
        return self.delta_thickness(js_prev, dt) / self.kappa

    def delta_batteryCap(self, js_prev, dt):
        return self.b_cell.elec_n.A * self.b_cell.elec_n.L * dt * js_prev

    def solve(self, I, dt):
        # solves for one time step
        if I < 0:
            self.j_s_prev = self.solve_j_s(I)
            self.resistance += self.delta_resistance(js_prev=self.j_s_prev, dt=dt)
        else:
            self.j_s_prev = 0.0
            self.resistance += 0.0

    def __repr__(self):
        return f"SEI with resistance {self.resistance}"






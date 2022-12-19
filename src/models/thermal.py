from src.battery_components.battery_cell import BatteryCell


class Lumped:
    def __init__(self, b_cell):
        # check for input arguments
        if not isinstance(b_cell, BatteryCell):
            raise TypeError("b_cell input argument needs to be a BatteryCell object.")
        # Assign class atributes
        self.b_cell = b_cell

    def reversible_heat(self, I, T):
        return I * T * (self.b_cell.elec_p.dOCPdT - self.b_cell.elec_n.dOCPdT)

    def irreversible_heat(self, I, V):
        return I * (V - (self.b_cell.elec_p.OCP - self.b_cell.elec_p.OCP))

    def heat_flux(self, T):
        return self.b_cell.h * self.b_cell.A * (T - self.b_cell.T_amb)

    def heat_balance(self, V, I):
        def func_heat_balance(T, t):
            main_coeff = 1 / (self.b_cell.rho * self.b_cell.Vol * self.b_cell.C_p)
            return main_coeff * (self.reversible_heat(I=I, T=T) + self.irreversible_heat(I=I, V=V) - self.heat_flux(T=T))
        return func_heat_balance

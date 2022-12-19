import pandas as pd

from src.battery_components import electrode


class Electrolyte:
    def __init__(self, file_path):
        # Read csv and parse for parameters
        df = electrode.Electrode.parse_csv(file_path=file_path)
        self.conc = df['Conc. [mol m^-3]']
        self.L = df['Thickness [m]']
        self.kappa = df['Ionic Conductivity [S m^-1]']
        self.epsilon = df['Volume Fraction']
        self.brugg = df['Bruggerman Coefficient']
        self.kappa_eff = self.kappa * (self.epsilon ** self.brugg)
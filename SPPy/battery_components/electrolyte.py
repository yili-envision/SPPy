import pandas as pd

from SPPy.battery_components import electrode


class Electrolyte:
    """
    Class for the Electrolyte object and contains the relevant parameters.
    """
    def __init__(self, file_path):
        """
        Constructor for the Electrolyte class.
        :param file_path: file_path to the csv containing the electrolyte parameters. Please adhere to the csv format
        in the data/param_electrolyte.csv file.
        """
        # Read csv and parse for parameters
        df = electrode.Electrode.parse_csv(file_path=file_path)
        self.conc = df['Conc. [mol m^-3]']
        self.L = df['Thickness [m]']
        self.kappa = df['Ionic Conductivity [S m^-1]']
        self.epsilon = df['Volume Fraction']
        self.brugg = df['Bruggerman Coefficient']
        self.kappa_eff = self.kappa * (self.epsilon ** self.brugg)
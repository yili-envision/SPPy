from dataclasses import dataclass

from SPPy.battery_components.parameter_set_manager import ParameterSets


@dataclass
class Electrolyte_:
    """
    Class for the Electrolyte object and contains the relevant electrolyte parameters.
    """
    conc: float  # electrolyte concentration, mol/m3
    L: float  # seperator thickness, m3
    kappa: float  # ionic conductivity, S/m
    epsilon: float  # electrolyte volume fraction

    def __post_init__(self):
        # Check for types of the input parameters
        if not isinstance(self.conc, float):
            raise "Electrolyte conc. needs to be a float."
        if not isinstance(self.L, float):
            raise "Electrolyte thickness needs to be a float."
        if not isinstance(self.kappa, float):
            raise "Electrolyte conductivity needs to be a float."
        if not isinstance(self.epsilon, float):
            raise "Electrolyte volume fraction needs to be a float."
        if not isinstance(self.brugg, float):
            raise "Electrolyte's bruggerman coefficient needs to be a float."

    @ property
    def kappa_eff(self):
        return self.kappa * (self.epsilon ** self.brugg)


class Electrolyte(Electrolyte_):
    """
    Derived child of Electrolyte_
    updates the Electrolyte_ attributes from the file.
    """
    def __init__(self, file_path):
        # Read csv and parse for parameters
        df = ParameterSets.parse_csv(file_path=file_path)
        conc = df['Conc. [mol m^-3]']
        L = df['Thickness [m]']
        kappa = df['Ionic Conductivity [S m^-1]']
        epsilon = df['Volume Fraction']
        brugg = df['Bruggerman Coefficient']

        super().__init__(conc=conc, L=L, kappa=kappa, epsilon=epsilon, brugg=brugg)
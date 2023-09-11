""" electrolyte
Contains the classes and functionality for the electrolyte related object(s).
"""

__all__ = ['Electrolyte']

__author__ = 'Moin Ahmed'
__copywrite__ = 'Copywrite 2023 by Moin Ahmed. All rights reserved'
__status__ = 'deployed'


from dataclasses import dataclass


@dataclass
class Electrolyte:
    """
    Class for the Electrolyte object and contains the relevant electrolyte parameters.
    """
    L: float  # seperator thickness, m3
    conc: float  # electrolyte concentration, mol/m3
    kappa: float  # ionic conductivity, S/m
    epsilon: float  # electrolyte volume fraction
    brugg: float  # Bruggerman coefficient for electrolyte

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

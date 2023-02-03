import warnings


def threshold_potential_warning():
    warnings.warn("Threshold battery cell potential reached.")

def threshold_SOC_warning():
    warnings.warn("Threshold battery cell SOC reached.")
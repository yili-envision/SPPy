class InvalidSOCException(Exception):
    "Raised when SOC is smaller than 0 or greater than 1."
    pass


class InsufficientInputOperatingConditions(Exception):
    "Raised when time and current arrays are not present in the input argument."
    pass


class InvalidElectrodeType(Exception):
    "Raised when invalid electrode type is inputted"
    pass
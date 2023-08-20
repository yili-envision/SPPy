from dataclasses import dataclass, field
from abc import ABC, abstractmethod



@dataclass
class BaseCycler(ABC):
    time_elapsed: float = field(default=0.0)  # time elapsed during cycling
    SOC_LIB: float = field(default=0.0)  # present battery cell SOC
    SOC_LIB_min: float = field(default=0.0)  # minimum battery cell SOC
    SOC_LIB_max: float = field(default=1.0)  # maximum battery cell SOC
    charge_current: float = field(default=0.0)  # charge current [A]
    discharge_current: float = field(default=0.0)  # discharge current [A]
    rest_time: float = field(default=0.0)  # rest time for the step "rest" [s]
    num_cycles: int = field(default=0)  # number of cycles
    cycle_steps: list = field(default_factory=lambda: [])  # list containing the sequence of the steps in a cycle

    @abstractmethod
    def get_current(self, step_name: str, t: float) -> float:
        """
        Returns the current for a particular cycling step. It is only valid for constant current situations.
        :param step_name: (string) The cycling step name.
        :param t: (float) the time value at the current time step [s]
        :return: (double) The current value.
        """
        if step_name == "rest":
            return 0.0
        elif step_name == "charge":
            return self.charge_current
        elif step_name == "discharge":
            return self.discharge_current
        else:
            raise TypeError("Not a valid step name")

    def reset_time_elapsed(self):
        self.time_elapsed = 0.0

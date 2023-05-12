class BaseCycler:
    def __init__(self):
        self.time_elapsed = 0.0
        self.SOC_LIB = 0.0

    def get_current(self, step_name):
        """
        Returns the current for a particular cycling step. It is only valid for constant current situations.
        :param step_name: (string) The cycling step name.
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

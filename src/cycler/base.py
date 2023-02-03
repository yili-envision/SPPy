class BaseCycler:
    def __init__(self):
        self.time_elapsed = 0.0

    def get_current(self, step_name):
        if step_name == "rest":
            return 0.0
        elif step_name == "charge":
            return self.charge_current
        elif step_name == "discharge":
            return self.discharge_current
        else:
            raise TypeError("Not a valid step name")
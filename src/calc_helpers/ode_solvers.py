def euler(func, t_prev, y_prev, step_size):
    return y_prev + func(y_prev, t_prev) * step_size

def rk4(func, t_prev, y_prev, step_size):
    k1 = func(y_prev, t_prev)
    k2 = func(y_prev + 0.5*k1*step_size, t_prev + 0.5*step_size)
    k3 = func(y_prev + 0.5*k2*step_size, t_prev + 0.5*step_size)
    k4 = func(y_prev + k3*step_size, t_prev + step_size)
    return y_prev + (1/6.0) * (k1 + 2*k2 + 2*k3 + k4) * step_size

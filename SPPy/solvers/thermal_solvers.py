__author__ = 'Moin Ahmed'
__copywrite__ = 'Copywrite 2023 by Moin Ahmed. All rights are reserved.'
__status__ = 'deployed'


from SPPy.calc_helpers.ode_solvers import rk4
from SPPy.models.thermal import ECMLumped


def calc_cell_temp(t_prev: float, dt: float, temp_prev: float, V: float, I: float, rho: float, Vol: float,
                   C_p: float, OCV: float, dOCVdT: float, h: float, A: float, T_amb: float) -> float:
    """
    Solves for the heat balance using the ODE rk4 solver for the ECM model.
    :param t_prev: time at the previous time step [s]
    :param dt: time difference between the current and the previous time steps [s]
    :param temp_prev: temperature at the previous time step [K]
    :param V: Battery cell potential at the current time step [V]
    :param I: Applied battery current [A]
    :param rho: battery density (mostly for thermal modelling), kg/m3
    :param Vol: battery cell volume, m3
    :param C_p: specific heat capacity, J / (K kg)
    :param OCV: Open-circiut potential [V]
    :param dOCVdT: change of OCV with respect to the change in temperature [V/K]
    :param h: heat transfer coefficient, J / (S K)
    :param A: surface area, m2
    :param T_amb: ambient temperature [K]
    :return: (float) Battery cell temperature [K]
    """
    t_model = ECMLumped()
    func_heat_balance = t_model.heat_balance(V=V, I=I, rho=rho, Vol=Vol, C_p=C_p, OCV=OCV, dOCVdT=dOCVdT, h=h, A=A,
                                             T_amb=T_amb)
    return rk4(func=func_heat_balance, t_prev=t_prev, y_prev=temp_prev, step_size=dt)



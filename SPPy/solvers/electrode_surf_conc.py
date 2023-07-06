import numpy as np
from scipy.optimize import bisect

from SPPy.calc_helpers.constants import Constants
from SPPy.calc_helpers import ode_solvers
from SPPy.warnings_and_exceptions.custom_exceptions import InvalidElectrodeType


class EigenFuncExp:
    """
    This solver uses the Eigen Function Expansion method as detailed in ref 1 to calculate the electrode
    surface SOC. As such, it stores all the necessary variables required for the iterative calculations for all time
    steps. After initiating the class, the object instance can be called iteratively to solve for electrode surface SOC
    for all time steps.

    The equation solved is
        x_j_surf = x_ini + (1/5)*j_scaled + 3 * integration{D_sj * j_scaled / R_j ** 2} * dt +
                    summation{u_jk - 2 * scaled_j / lambda_k ** 2}
    In the above equation, the integration is performed from t=0 to the current time. Moreover, the summation is
    performed from k=1 to k=N. Here k represents the kth term of the solution series.

    Reference:
    1. Guo, M., Sikha, G., & White, R. E. (2011). Single-Particle Model for a Lithium-Ion Cell: Thermal Behavior.
    Journal of The Electrochemical Society, 158(2), A122. https://doi.org/10.1149/1.3521314/XML
    """

    def __init__(self, x_init: float, n: int, electrode_type: str):
        self.x_init_ = x_init  # initial electrode SOC
        self.N_ = n  # the number of terms in the solution series

        self.integ_term = 0  # the integration term, which is initialized as zero
        self.lst_u_k = [0 for i in range(self.N)]  # a list of solved values of eigenfunctions, the values of which are
        # all initialized to zero.

        if electrode_type == 'p' or electrode_type == 'n':
            self.electrode_type = electrode_type  # either positive electrode ('p') or negative electrode ('n').
        else:
            raise InvalidElectrodeType


    @property
    def x_init(self):
        """
        Initial electrode SOC
        :return: (float) Initial electrode SOC
        """
        return self.x_init_

    @property
    def N(self):
        """
        The number of terms in the solution series.
        :return: (int) number of terms in the solution series.
        """
        return self.N_

    @staticmethod
    def lambda_func(lambda_k):
        """
        Algebraic equation from which the eigenvalues can be calculated.
        :param lambda_k: (float) eigen value ot the kth term.
        :return: (float) the value of the elgebraic equation.
        """
        return np.sin(lambda_k) - lambda_k * np.cos(lambda_k)

    def lambda_bounds(self):
        """
        The list which contains the tuple containing the lower and upper bounds of the eigenvalues.
        :return: (list) list containing the tuple of bounds for the eigenvalues.
        """
        return [(np.pi * (1 + k), np.pi * (2 + k)) for k in range(self.N)]  # k refers to the kth term of the series

    @property
    def lambda_roots(self):
        """
        Uses the bisect method to solve for the eigenvalue algebraic equation within the bounds.
        :return: (list) list containing the eigenvalues for all solution terms.
        """
        bounds = self.lambda_bounds()
        return [bisect(self.lambda_func, bounds[k][0], bounds[k][1]) for k in range(self.N)]  # k refers to the kth
        # term of the series

    def j_scaled(self, i_app, R, S, D_s, c_smax):
        """
        Returns the dimensionless lithium-ion flux
        :return: (float) dimensionless lithium-ion flux
        """
        j_scaled_ = i_app * R / (Constants.F * S * D_s * c_smax)
        if self.electrode_type == 'p':
            return -j_scaled_
        elif self.electrode_type == 'n':
            return j_scaled_

    def update_integ_term(self, dt, i_app, R, S, D_s, c_smax):
        """
        Updates the integration term. Integration is performed using simple algebraic integration.
        :return: (float) updated integration term.
        """
        self.integ_term += 3 * (D_s * self.j_scaled(i_app=i_app, R=R, S=S, D_s=D_s, c_smax=c_smax) / (R ** 2)) * dt

    @staticmethod
    def u_k_expression(lambda_k, D, R, scaled_flux):
        """
        Returns a function that represents the eigenfunction ode.
        :param lambda_k: eigenvalue of the kth term
        :param D: diffusivity [m2/s]
        :param R: electrode particle radius [m]
        :param scaled_flux: dimensionless scaled lithium-ion flux
        :return: (func) a function representing the eigenfunction ode
        """
        def u_k_odeFunc(x, t):
            return -(lambda_k ** 2) * D * x / (R ** 2) + 2 * D * scaled_flux / (R ** 2)
        return u_k_odeFunc

    def solve_u_k(self, root_value, t_prev, dt, u_k_prev, i_app, R, S, D_s, c_smax):
        """
        Calculates the eigenfunction value from the eigen values using the ode function. This ode function is solved
        using the rk4 ode solver.
        :param root_value:
        :param t_prev:
        :param u_k_j_prev:
        :param dt:
        :return:
        """
        j_scaled_ = self.j_scaled(i_app=i_app, R=R, S=S, D_s=D_s, c_smax=c_smax)
        u_k_p_func = self.u_k_expression(lambda_k=root_value, D=D_s, R=R, scaled_flux=j_scaled_)
        return ode_solvers.rk4(func=u_k_p_func, t_prev=t_prev, y_prev=u_k_prev, step_size=dt)

    def get_summation_term(self, dt, t_prev, i_app, R, S, D_s, c_smax):
        """
        Calculates and returns the summation term of the Eigen Expansion equation.
        :param t_prev:
        :param dt:
        :param j_scaled:
        :return:
        """
        sum_term = 0
        # Solve for the eigenfunction for all roots using the iteration below:
        j_scaled_ = self.j_scaled(i_app=i_app, R=R, S=S, D_s=D_s, c_smax=c_smax)
        for iter_root, root_value in enumerate(self.lambda_roots):
            self.lst_u_k[iter_root] = self.solve_u_k(root_value=root_value, t_prev=t_prev,
                                                     u_k_prev=self.lst_u_k[iter_root], dt=dt,
                                                     i_app=i_app, R=R, S=S, D_s=D_s, c_smax=c_smax)
            sum_term += self.lst_u_k[iter_root] - (2 * j_scaled_ / (root_value ** 2))
        return sum_term

    def calc_SOC_surf(self, dt, t_prev, i_app, R, S, D_s, c_smax):
        """
        Calculates the electrode surface SOC using the Eigen Expansion method.
        :param dt: The time difference between the current and the previous time steps [s].
        :param t_prev: Time value of the previous time step [s].
        :return: (float) The electrode's surface SOC.
        """
        j_scaled_ = self.j_scaled(i_app=i_app, R=R, S=S, D_s=D_s, c_smax=c_smax)
        sum_term = self.get_summation_term(t_prev=t_prev, dt=dt, i_app=i_app, R=R, S=S, D_s=D_s, c_smax=c_smax)
        self.update_integ_term(dt=dt, i_app=i_app, R=R, S=S, D_s=D_s, c_smax=c_smax)
        return self.x_init + j_scaled_ / 5 + self.integ_term + sum_term

    def __call__(self, dt, t_prev, i_app, R, S, D_s, c_smax):
        """
        This method calculates the electrode surface SOC
        :param dt: Time difference between current and previous time steps [s].
        :param t_prev: Time value at the previous time step [s].
        :param i_app: Applied current at the current time step [A].
        :param R:  Electrode particle radius [m]
        :param S: Electrode electroactive area [m2]
        :param D_s: Electrode diffusivity [m2/s]
        :param c_smax: Electrode max. conc [mol/m3]
        :return: (float) The electrode's surface SOC.
        """
        return self.calc_SOC_surf(dt=dt, t_prev=t_prev, i_app=i_app, R=R, S=S, D_s=D_s, c_smax=c_smax)

import unittest

from SPPy.solvers.electrode_surf_conc import PolynomialApproximation

# Electrode parameters below
R = 1.25e-5  # electrode particle radius in [m]
c_max = 31833  # max. electrode concentration [mol/m3]
D = 3.9e-14  # electrode diffusivity [m2/s]
S = 0.7824  # electrode electrochemical active area [m2]
SOC_init = 0.7568  # initial electrode SOC

poly_solver1 = PolynomialApproximation(c_init=SOC_init*c_max, electrode_type='n', type='two')
poly_solver2 = PolynomialApproximation(c_init=SOC_init*c_max, electrode_type='n', type='higher')

# Simulation parameters below
t_prev = 0  # previous time [s]
dt = 0.1  # in s

# solve for SOC wrt to time
lst_time_poly, lst_poly_solver1, lst_poly_solver2 = [], [], []
SOC_poly1 = SOC_init
while SOC_poly1 > 0:
    SOC_poly1 = poly_solver1(dt=dt, t_prev=t_prev, i_app=-1.65, R=R, S=S, D_s=D, c_smax=c_max)
    SOC_poly2 = poly_solver2(dt=dt, t_prev=t_prev, i_app=-1.65, R=R, S=S, D_s=D, c_smax=c_max)
    lst_time_poly.append(t_prev)
    lst_poly_solver1.append(SOC_poly1)
    lst_poly_solver2.append(SOC_poly2)
    print(SOC_poly2)

    t_prev += dt  # update the time

class TestPolyApprox(unittest.TestCase):
    def test_constructor(self):
        pass

    def test_solve(self):
        self.assertEqual(0.7127702012060186, lst_poly_solver1[0])
        self.assertEqual(0.7127537226189332, lst_poly_solver1[1])

        self.assertEqual(0.7504676658078573, lst_poly_solver2[0])

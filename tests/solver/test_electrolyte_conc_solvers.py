import unittest


from SPPy.solvers.electrolyte_conc import ElectrolyteFVMCoordinates


class TestElectrolyteFVMCoordinates(unittest.TestCase):
    instance = ElectrolyteFVMCoordinates(D_e=7.5e-10, epsilon_en=0.385, epsilon_esep=0.785, epsilon_ep=0.485,
                                         L_n=8e-5, L_s=2.5e-5, L_p=8.8e-5, brugg=4)

    def test_array_xn(self):
        self.assertEqual(8e-5 / 10, self.instance.dx_n)
        self.assertAlmostEqual(4e-6, self.instance.array_x_n[0])
        self.assertAlmostEqual(4e-6 + 1 * 8e-6, self.instance.array_x_n[1])
        self.assertAlmostEqual(4e-6 + 2 * 8e-6, self.instance.array_x_n[2])
        self.assertAlmostEqual(4e-6 + 3 * 8e-6, self.instance.array_x_n[3])
        self.assertAlmostEqual(4e-6 + 4 * 8e-6, self.instance.array_x_n[4])
        self.assertAlmostEqual(4e-6 + 5 * 8e-6, self.instance.array_x_n[5])
        self.assertAlmostEqual(4e-6 + 6 * 8e-6, self.instance.array_x_n[6])
        self.assertAlmostEqual(4e-6 + 7 * 8e-6, self.instance.array_x_n[7])
        self.assertAlmostEqual(4e-6 + 8 * 8e-6, self.instance.array_x_n[8])
        self.assertAlmostEqual(4e-6 + 9 * 8e-6, self.instance.array_x_n[9])
        self.assertAlmostEqual(10, len(self.instance.array_x_n))

    def test_array_xs(self):
        self.assertEqual(2.5e-5 / 10, self.instance.dx_s)
        self.assertAlmostEqual(8e-5 + 1.25e-6, self.instance.array_x_s[0])
        self.assertAlmostEqual(8e-5 + 1.25e-6 + 1 * self.instance.dx_s, self.instance.array_x_s[1])
        self.assertAlmostEqual(8e-5 + 1.25e-6 + 2 * self.instance.dx_s, self.instance.array_x_s[2])
        self.assertAlmostEqual(8e-5 + 1.25e-6 + 3 * self.instance.dx_s, self.instance.array_x_s[3])
        self.assertAlmostEqual(8e-5 + 1.25e-6 + 4 * self.instance.dx_s, self.instance.array_x_s[4])
        self.assertAlmostEqual(8e-5 + 1.25e-6 + 5 * self.instance.dx_s, self.instance.array_x_s[5])
        self.assertAlmostEqual(8e-5 + 1.25e-6 + 6 * self.instance.dx_s, self.instance.array_x_s[6])
        self.assertAlmostEqual(8e-5 + 1.25e-6 + 7 * self.instance.dx_s, self.instance.array_x_s[7])
        self.assertAlmostEqual(8e-5 + 1.25e-6 + 8 * self.instance.dx_s, self.instance.array_x_s[8])
        self.assertAlmostEqual(8e-5 + 1.25e-6 + 9 * self.instance.dx_s, self.instance.array_x_s[9])
        self.assertAlmostEqual(10, len(self.instance.array_x_s))

    def test_array_xp(self):
        self.assertEqual(8.8e-5 / 10, self.instance.dx_p)
        self.assertAlmostEqual(1.05e-4 + 4.4e-6, self.instance.array_x_p[0])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 1 * self.instance.dx_p, self.instance.array_x_p[1])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 2 * self.instance.dx_p, self.instance.array_x_p[2])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 3 * self.instance.dx_p, self.instance.array_x_p[3])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 4 * self.instance.dx_p, self.instance.array_x_p[4])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 5 * self.instance.dx_p, self.instance.array_x_p[5])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 6 * self.instance.dx_p, self.instance.array_x_p[6])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 7 * self.instance.dx_p, self.instance.array_x_p[7])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 8 * self.instance.dx_p, self.instance.array_x_p[8])
        self.assertAlmostEqual(1.05e-4 + 4.4e-6 + 9 * self.instance.dx_p, self.instance.array_x_p[9])
        self.assertAlmostEqual(10, len(self.instance.array_x_s))

    def test_array_dx(self):
        self.assertEqual(self.instance.dx_n, self.instance.array_dx[0])
        self.assertEqual(self.instance.dx_n, self.instance.array_dx[5])
        self.assertEqual(self.instance.dx_n, self.instance.array_dx[9])

        self.assertEqual(self.instance.dx_s, self.instance.array_dx[11])
        self.assertEqual(self.instance.dx_s, self.instance.array_dx[15])
        self.assertEqual(self.instance.dx_s, self.instance.array_dx[18])

        self.assertEqual(self.instance.dx_p, self.instance.array_dx[20])
        self.assertEqual(self.instance.dx_p, self.instance.array_dx[25])
        self.assertEqual(self.instance.dx_p, self.instance.array_dx[-1])
        self.assertEqual(30, len(self.instance.array_dx))

    def test_array_epsilon(self):
        print(self.instance.array_epsilon_e)

    def test_array_D_eff(self):
        print(self.instance.array_D_eff)

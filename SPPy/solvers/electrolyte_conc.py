import numpy.typing as npt

from SPPy.calc_helpers.matrix_operations import TDMAsolver


class ElectrolyteConcSolver:
    def __init__(self, electrolyte_instance: Electrolyte):
        self.electrolyte = electrolyte_instance

    def diags(self, dt: float):
        # initialize the diagonals
        diag_elements = []
        upper_diag_elements = []
        lower_diag_elements = []
        # update first elements
        dx = (self.electrolyte.array_x[1] - self.electrolyte.array_x[0])
        D1 = self.electrolyte.array_D_eff[0]
        D2 = self.electrolyte.array_D_eff[1]
        A = dt / (2 * self.electrolyte.array_dx[0])
        diag_elements.append(self.electrolyte.epsilon_e[0] + A * (D2 + D1) / dx)
        upper_diag_elements.append(-A * (D2 + D1) / dx)
        for i in range(1, len(self.electrolyte.array_x) - 1):
            dx1 = self.electrolyte.array_x[i] - self.electrolyte.array_x[i - 1]
            dx2 = self.electrolyte.array_x[i + 1] - self.electrolyte.array_x[i]
            D1 = self.electrolyte.array_D_eff[i - 1]
            D2 = self.electrolyte.array_D_eff[i]
            D3 = self.electrolyte.array_D_eff[i + 1]
            A = dt / (2 * self.electrolyte.array_dx[i])
            diag_elements.append(self.electrolyte.epsilon_e[i] + A * ((D1 + D2) / dx1 + (D2 + D3) / dx2))
            upper_diag_elements.append(-A * (D3 + D2) / dx2)
            lower_diag_elements.append(-A * (D1 + D2) / dx1)
        # update last elements
        dx = (self.electrolyte.array_x[-1] - self.electrolyte.array_x[-2])
        D1 = self.electrolyte.array_D_eff[-1]
        D2 = self.electrolyte.array_D_eff[-1]
        A = dt / (2 * self.electrolyte.array_dx[-1])
        diag_elements.append(self.electrolyte.epsilon_e[-1] + A * (D2 + D1) / dx)
        lower_diag_elements.append(-A * (D2 + D1) / dx)
        return lower_diag_elements, diag_elements, upper_diag_elements

    def M_ce(self, dt) -> npt.ArrayLike:
        l_diag, diag, u_diag = self.diags(dt)
        return np.diag(diag) + np.diag(u_diag, 1) + np.diag(l_diag, -1)

    def ce_j_vec(self, c_prev: npt.ArrayLike, j: npt.ArrayLike, dt: float, a_s: npt.ArrayLike) -> npt.ArrayLike:
        ce_j_vec_1_ = (c_prev * self.electrolyte.epsilon_e).reshape(-1, 1)
        ce_j_vec_2_ = ((1 - self.electrolyte.transference) * a_s * j * dt).reshape(-1, 1)
        return ce_j_vec_1_ + ce_j_vec_2_

    def solve_ce(self, c_prev, j, dt, a_s, solver_method:str ='TDMA') -> npt.ArrayLike:
        b = self.ce_j_vec(c_prev=c_prev, j=j, dt=dt, a_s=a_s)
        if solver_method == 'TDMA':
            l_diag, diag, u_diag = self.diags(dt)
            return TDMAsolver(l_diag=l_diag, diag=diag, u_diag=u_diag, col_vec=b)
        elif solver_method == 'inverse':
            M = np.linalg.inv(self.M_ce(dt=dt))
            return np.ndarray.flatten(M @ b)

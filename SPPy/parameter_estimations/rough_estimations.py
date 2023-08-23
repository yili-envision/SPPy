import pickle
import os
from typing import Optional

import numpy.typing as npt
import matplotlib.pyplot as plt

import SPPy
from SPPy.cycler.base import BaseCycler
from SPPy.calc_helpers.numerical_diff import first_centered_FD


class GridSearch:
    def __init__(self, parameter_set_name: str, SOC_init_p: float, SOC_init_n: float, T: float, i_cycler: BaseCycler):
        self.parameter_set_name = parameter_set_name
        self.SOC_init_p = SOC_init_p
        self.SOC_init_n = SOC_init_n
        self.T = T
        self.i_cycler = i_cycler

    @classmethod
    def save_meta_data(cls, file_name: str, sol_name: str,
                       R_p: float, R_n: float,
                       c_pmax: float, c_nmax: float,
                       D_p: float, D_n: float) -> None:
        with open(file_name, "a") as file:
            file.write(f"{sol_name},{R_p},{R_n},{c_pmax},{c_nmax},{D_p},{D_n}")
            file.write("\n")

    def generate_data(self,
                      array_R_p: npt.ArrayLike, array_R_n: npt.ArrayLike,
                      array_c_pmax: npt.ArrayLike, array_c_nmax: npt.ArrayLike,
                      array_D_p: npt.ArrayLike, array_D_n: npt.ArrayLike,
                      save_results: bool = True, index_start: int = 1,
                      dir_name: str = 'grid_search_results') -> None:
        index = index_start
        for R_p in array_R_p:
            for R_n in array_R_n:
                for c_pmax in array_c_pmax:
                    for c_nmax in array_c_nmax:
                        for D_p in array_D_p:
                            for D_n in array_D_n:
                                cell = SPPy.BatteryCell(self.parameter_set_name, self.SOC_init_p,
                                                        self.SOC_init_n, self.T)

                                cell.elec_p.R = R_p
                                cell.elec_p.max_conc = c_pmax
                                cell.elec_n.R = R_n
                                cell.elec_n.max_conc = c_nmax
                                cell.elec_p.D_ref = D_p
                                cell.elec_n.D_ref = D_n

                                solver = SPPy.SPPySolver(b_cell=cell, N=5, isothermal=True, degradation=False,
                                                         electrode_SOC_solver='poly')

                                # simulate and save
                                self.i_cycler.reset()
                                sol = solver.solve(cycler_instance=self.i_cycler, t_increment=1)
                                sol_name = f'sol{index}'
                                if save_results:
                                    sol.save_instance(os.path.join(dir_name, sol_name))
                                    self.save_meta_data(os.path.join(dir_name, 'meta.txt'),
                                                        sol_name=sol_name,
                                                        R_p=R_p,
                                                        R_n=R_n,
                                                        c_pmax=c_pmax,
                                                        c_nmax=c_nmax,
                                                        D_p=D_p,
                                                        D_n=D_n)

                                # Update loop variables below
                                index += 1

    @classmethod
    def plot_generated_data(cls, lst_sol_num: list, file_dir: str = "grid_search_results/",
                            t_exp: Optional[npt.ArrayLike] = None, V_exp: Optional[npt.ArrayLike] = None,
                            show_legends: str = False,
                            index_start: int = -1):
        fig = plt.figure(figsize=(10,6))
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)
        # FILE_DIR = f'{file_dir}sol*'
        # if index_start > 0:
        #     FILE_DIR = f'{file_dir}sol{index_start}*'
        for i, sol_num in enumerate(lst_sol_num):
            FILE_DIR = os.path.join(file_dir, f'sol{sol_num}')
            with open(FILE_DIR, "rb") as solfile:
                sol = pickle.load(solfile)
            label = os.path.basename(FILE_DIR)
            ax1.plot(sol.t, sol.V, label=label, linewidth=3)
            ax2.plot(sol.t[1:-1], first_centered_FD(array_x=sol.V, array_t=sol.t), label=label, linewidth=3)
        if t_exp is not None:
            label = 'exp'
            ax1.plot(t_exp, V_exp, label=label, linewidth=3)
            from scipy.signal import savgol_filter
            y=first_centered_FD(array_x=V_exp, array_t=t_exp)
            yhat = savgol_filter(y, 1000, 3)  # window size 51, polynomial order 3
            ax2.plot(t_exp[1:-1], yhat, label=label, linewidth=3)

        if show_legends:
            ax1.legend()
            ax2.legend()

        plt.tight_layout()
        plt.show()

import numpy.typing as npt


def TDMAsolver(l_diag: npt.ArrayLike, diag: npt.ArrayLike, u_diag: npt.ArrayLike, col_vec: npt.ArrayLike) -> npt.ArrayLike:
    '''
    TDMA (a.k.a Thomas algorithm) solver for tridiagonal system of equations.
    Code Modified from:
    https://gist.github.com/cbellei/8ab3ab8551b8dfc8b081c518ccd9ada9?permalink_comment_id=3109807
    '''
    nf = len(col_vec)  # number of equations
    c_l_diag, c_diag, c_u_diag, c_col_vec = map(np.array, (l_diag, diag, u_diag, col_vec))  # copy arrays
    for it in range(1, nf):
        mc = c_l_diag[it - 1] / c_diag[it - 1]
        c_diag[it] = c_diag[it] - mc * c_u_diag[it - 1]
        c_col_vec[it] = c_col_vec[it] - mc * c_col_vec[it - 1]

    xc = c_diag
    xc[-1] = c_col_vec[-1] / c_diag[-1]

    for il in range(nf - 2, -1, -1):
        xc[il] = (c_col_vec[il] - c_u_diag[il] * xc[il + 1]) / c_diag[il]
    return xc

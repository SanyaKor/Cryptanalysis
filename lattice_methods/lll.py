import numpy as np
from lattice_methods.utils import gram_schmidt

def lll_reduce(basis, delta=0.75, verbose=False):

    basis = [b.copy() for b in basis]
    n = len(basis)
    k = 1


    while k < n:

        ortho, mu = gram_schmidt(basis)

        for j in range(k - 1, -1, -1):  # j < k

            if abs(mu[k, j]) > 0.5:
                r = round(mu[k, j])
                basis[k] -= r * basis[j]
                ortho, mu = gram_schmidt(basis)

        norm_sq_prev = np.dot(ortho[k - 1], ortho[k - 1])
        norm_sq_curr = np.dot(ortho[k], ortho[k])

        lhs = delta * norm_sq_prev
        rhs = norm_sq_curr + mu[k, k - 1]**2 * norm_sq_prev

        if lhs > rhs:
            basis[k], basis[k - 1] = basis[k - 1], basis[k].copy()

            k = max(k - 1, 1)
        else:
            k += 1

    return basis




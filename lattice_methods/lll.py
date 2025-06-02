"""
Implementation of the classical LLL lattice basis reduction algorithm.

Module author: Aleksandr Lebedev <alebede1@hs-mittweida.de>

This module provides an implementation of the Lenstra–Lenstra–Lovász (LLL) algorithm
for lattice basis reduction. It uses Gram-Schmidt orthogonalization to iteratively
reduce a given basis to a shorter and more orthogonal form.
"""

import numpy as np
from lattice_methods.utils import gram_schmidt

def lll_reduce(basis, delta=0.75, verbose=False):
    """
    Performs LLL (Lenstra–Lenstra–Lovász) lattice basis reduction.

    This function applies the classical LLL algorithm to reduce a given lattice basis
    to a shorter and nearly orthogonal form.

    :param basis: A list of NumPy vectors representing the lattice basis.
    :type basis: list[numpy.ndarray]
    :param delta: Lovász parameter, typically in the range (0.5, 1). Default is 0.75.
    :type delta: float
    :param verbose: If True, enables step-by-step debug output (currently unused).
    :type verbose: bool

    :return: A list of NumPy vectors representing the LLL-reduced lattice basis.
    :rtype: list[numpy.ndarray]

    .. note::
       This function assumes all basis vectors are linearly independent.

    .. warning::
       No validation is performed on the input; ensure basis vectors are valid.

    .. seealso::
       :func:`lattice_methods.utils.gram_schmidt` for orthogonalization.
    """

    ##TODO verbose ..

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




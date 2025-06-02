"""
Utility functions for lattice basis analysis and reduction.

This module provides general-purpose linear algebra utilities with a focus
on lattice-related operations. Designed for extensibility in cryptographic,
geometric, or numerical applications.

Module author: Aleksandr Lebedev <alebede1@hs-mittweida.de>

Date: 2025-05-28
"""

import numpy as np


def are_bases_equivalent(basis1, basis2):
    """
    Checks whether two bases generate the same lattice via unimodular transformation.

    Determines whether there exists an integer matrix T with determinant ±1 such that:
    ``basis2 = basis1 @ T``

    :param basis1: First basis, as a list of NumPy vectors.
    :type basis1: list[numpy.ndarray]
    :param basis2: Second basis, as a list of NumPy vectors.
    :type basis2: list[numpy.ndarray]

    :return: True if both bases generate the same lattice, False otherwise.
    :rtype: bool

    :raises ValueError: If the input bases are not square (i.e., n vectors in ℝⁿ).

    .. note::
       This function checks for a unimodular transformation between the two bases.
    """

    basis1 = np.column_stack(basis1)
    basis2 = np.column_stack(basis2)

    if basis1.shape != basis2.shape or basis1.shape[0] != basis1.shape[1]:
        raise ValueError("Both bases must be square matrices (n vectors of dim n).")

    try:
        T = np.linalg.solve(basis1, basis2)
    except np.linalg.LinAlgError:
        return False


    return np.allclose(T, np.round(T)) and round(abs(np.linalg.det(T))) == 1

def gram_schmidt(basis):
    """
    Applies Gram-Schmidt orthogonalization to a lattice basis.

    This function computes an orthogonal basis from the given list of lattice vectors
    using the classical Gram-Schmidt process. It also returns the matrix of Gram-Schmidt
    coefficients used in the process.

    :param basis: List of NumPy vectors representing the lattice basis.
    :type basis: list[numpy.ndarray]

    :return: A tuple (ortho, mu), where:
             - ortho: List of orthogonalized basis vectors.
             - mu: Matrix of Gram-Schmidt coefficients.
    :rtype: tuple[list[numpy.ndarray], numpy.ndarray]

    .. note::
       The orthogonalized vectors are not necessarily part of the lattice;
       they span the same space but are not required to have integer coordinates.
    """

    n = len(basis)
    dim = len(basis[0])

    ortho = [np.zeros(dim) for _ in range(n)]
    mu = np.zeros((n, n))

    for i in range(n):
        b_i = basis[i]
        projection = np.zeros(dim,  dtype=object)

        for j in range(i):
            mu[i, j] = np.dot(b_i, ortho[j]) / np.dot(ortho[j], ortho[j])
            projection += mu[i, j] * ortho[j]

        ortho[i] = b_i - projection

    return ortho, mu


def are_bases_equal_2d(basis1, basis2):
    """
    Checks whether two 2D bases are equal up to sign and order.

    :param basis1: First 2D basis (list of 2 vectors).
    :type basis1: list[numpy.ndarray]
    :param basis2: Second 2D basis (list of 2 vectors).
    :type basis2: list[numpy.ndarray]

    :return: True if bases contain the same vectors (signs and order ignored), False otherwise.
    :rtype: bool
    """
    def normalize(v):
        v = np.array(v)
        return v if v[0] > 0 or (v[0] == 0 and v[1] >= 0) else -v

    def sorted_basis(u, v):
        return sorted([normalize(u).tolist(), normalize(v).tolist()])

    return sorted_basis(basis1[0], basis1[1]) == sorted_basis(basis2[0], basis2[1])


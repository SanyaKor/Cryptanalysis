"""
Implementation of a basic two-dimensional lattice basis reduction algorithm.

Module author: Aleksandr Lebedev <alebede1@hs-mittweida.de>
Date: 2025-05-28
"""

import numpy as np

def reduce_2d_basis(basis1, basis2, verbose=False):
    """
    Performs Gauss-style reduction of a 2D lattice basis.

    This function reduces a two-dimensional lattice basis using a simplified form
    of Gauss' lattice basis reduction algorithm. The process iteratively subtracts
    integer multiples of vectors to produce a shorter, more orthogonal basis.

    :param basis1: First basis vector.
    :type basis1: numpy.ndarray
    :param basis2: Second basis vector.
    :type basis2: numpy.ndarray
    :param verbose: If True, returns a log of each reduction step.
    :type verbose: bool

    :return:
        If verbose is False, returns a list [b1, b2] representing the reduced basis.
        If verbose is True, returns a list of dictionaries with reduction steps, where each dictionary contains:

            - 'step' (str or int): Iteration index or '→ shortest'
            - 'b1' (numpy.ndarray): Current first basis vector
            - 'b2' (numpy.ndarray): Current second basis vector
    :rtype: list

    .. note::
       The algorithm terminates when the projection coefficient `t` becomes zero.
       This is a simplified form of Gauss’ lattice basis reduction in 2D.
    """
    data = []

    steps = 0

    #TODO linear ind check
    # if np.linalg.matrix_rank(np.column_stack((basis1, basis2))) < 2:
    #     raise ValueError("Input vectors are linearly dependent.")

    while True:

        if np.linalg.norm(basis2) < np.linalg.norm(basis1):
            basis1, basis2 = basis2, basis1
            continue


        t = round(np.dot(basis1, basis2) / np.dot(basis1, basis1))

        data.append({
            'step': steps,
            'b1': basis1.copy(),
            'b2': basis2.copy(),
        })

        steps += 1


        if t == 0:
            break

        basis2 = basis2 - t * basis1

    shortest = basis1 if np.linalg.norm(basis1) <= np.linalg.norm(basis2) else basis2

    ###TODO reducing the basis not includes short vector, might have to remove
    data.append({
        'step': '→ shortest',
        'b1': shortest if np.array_equal(shortest, basis1) else '',
        'b2': shortest if np.array_equal(shortest, basis2) else ''
    })

    return data if verbose else [basis1, basis2]
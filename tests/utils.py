import numpy as np


def generate_random_bases(n=10, dim=2, min_abs=10, max_val=50):

    bases = []

    while len(bases) < n:
        basis = [np.random.randint(-max_val, max_val + 1, size=dim) for _ in range(dim)]

        all_coords = np.concatenate(basis)
        if any(abs(x) < min_abs for x in all_coords):
            continue

        matrix = np.column_stack(basis)
        if np.linalg.matrix_rank(matrix) == dim:
            bases.append(tuple(basis))

    return bases
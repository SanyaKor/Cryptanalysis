import numpy as np


def are_bases_equivalent(basis1, basis2):

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
    def normalize(v):
        v = np.array(v)
        return v if v[0] > 0 or (v[0] == 0 and v[1] >= 0) else -v

    def sorted_basis(u, v):
        return sorted([normalize(u).tolist(), normalize(v).tolist()])

    return sorted_basis(basis1[0], basis1[1]) == sorted_basis(basis2[0], basis2[1])


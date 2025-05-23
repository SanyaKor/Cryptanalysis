import numpy as np

def reduce_2d_basis(basis1, basis2, verbose=False):

    data = []

    steps = 0

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
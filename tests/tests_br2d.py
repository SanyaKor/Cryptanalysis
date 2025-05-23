from lattice_methods.basis_reduction_2d import reduce_2d_basis
from lattice_methods.utils import are_bases_equivalent
import numpy as np

def tests_br2d(basis_list, verbose=False):

    tests_amount = len(basis_list)
    tests_passed = 0

    results = []

    for i, (b1, b2) in enumerate(basis_list):

        b1_reduced, b2_reduced = reduce_2d_basis(b1, b2)

        same = are_bases_equivalent([b1, b2], [b1_reduced, b2_reduced])

        original_len = min(np.linalg.norm(b1), np.linalg.norm(b2))
        reduced_len = min(np.linalg.norm(b1_reduced), np.linalg.norm(b2_reduced))
        improved = reduced_len <= original_len

        if same and improved:
            tests_passed += 1
            if verbose:
                print(f"✅ Test {i + 1}: PASSED")
                print(f"Initial basis: b1 = {b1}, b2 = {b2}")
                print(f"Reduced basis: b1 = {b1_reduced}, b2 = {b2_reduced}")

            results.append({
                "b1": b1_reduced,
                "b2": b2_reduced,
                "result": 1
            })

        else:

            if verbose:
                print(f"❌ Test {i + 1} FAILED: ")
                print(f"b1 = {b1}, b2 = {b2}")

            results.append({
                    "b1": b1_reduced,
                    "b2": b2_reduced,
                    "result": 0
            })
    if verbose:
        print(f"\n📊 {tests_amount}/{tests_passed} tests passed.")

    return results
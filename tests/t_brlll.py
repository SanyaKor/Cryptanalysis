from lattice_methods.lll import lll_reduce
from lattice_methods.utils import are_bases_equivalent
import numpy as np

def t_brlll(basis_list, verbose=False):

    tests_amount = len(basis_list)
    tests_passed = 0

    results = []

    for i, basis in enumerate(basis_list):
        reduced = lll_reduce(basis)

        same = are_bases_equivalent(basis, reduced)

        original_len = min(np.linalg.norm(v) for v in basis)
        reduced_len = min(np.linalg.norm(v) for v in reduced)
        improved = reduced_len <= original_len

        result = int(same and improved)
        if result:
            tests_passed += 1

        if verbose:
            print(f"{'✅' if result else '❌'} Test {i + 1}: {'PASSED' if result else 'FAILED'}")
            print("Initial basis:")
            for v in basis:
                print(" ", v)
            print("Reduced basis:")
            for v in reduced:
                print(" ", v)
            print()

        results.append({
            "basis": [v.tolist() for v in reduced],
            "result": result
        })

    if verbose:
        print(f"\n📊 {tests_passed}/{tests_amount} tests passed.")

    return results
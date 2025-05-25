## 📦 Dependencies

This project relies on external Python libraries listed in the `requirements.txt` file.  
To install them, use the following command:

```bash
pip install -r requirements.txt
```


📘 **Usage Examples:** See [notebooks/usage_examples.ipynb](notebooks/usage_examples.ipynb)  
for practical demonstrations of lattice reduction functions (`reduce_2d_basis`, `lll_reduce`, etc.).

✅ **Test Cases:** See [notebooks/tests.ipynb](notebooks/tests.ipynb)  
for automated tests validating correctness of the algorithms.

📝 **Exercises from Literature:** See [notebooks/Exercises.ipynb](notebooks/Exercises.ipynb)  
contains solved exercises from *Introduction to Cryptography with Coding Theory* (Trappe & Washington).

🛠️ **Core Implementations:** See [lattice_methods](lattice_methods)  
This directory contains the core Python implementations for:
- `reduce_2d_basis` — basic 2D lattice reduction
- `lll_reduce` — LLL lattice basis reduction algorithm
- `ntru_*` — NTRU cryptosystem (keygen, encryption, decryption)
- utility functions for validation and formatting and etc


### 📚 References

- **Introduction to Cryptography with Coding Theory**  
  Trappe, W., & Washington, L. C. — 2nd Edition, Pearson, 2006.

- **NTRU: A Ring-Based Public Key Cryptosystem**  
  Hoffstein, J., Pipher, J., & Silverman, J. H., 1998.  
  [https://ntru.org](https://ntru.org)

- **Lenstra–Lenstra–Lovász lattice basis reduction algorithm**  
  Wikipedia Article.  
  [https://en.wikipedia.org/wiki/Lenstra%E2%80%93Lenstra%E2%80%93Lov%C3%A1sz_lattice_basis_reduction_algorithm](https://en.wikipedia.org/wiki/Lenstra%E2%80%93Lenstra%E2%80%93Lov%C3%A1sz_lattice_basis_reduction_algorithm)

- **Public Key Cryptography – NTRU**  
  Tengely, Sz. — Example values used in this notebook are based on:  
  [https://shrek.unideb.hu/~tengely/crypto/section-8.html](https://shrek.unideb.hu/~tengely/crypto/section-8.html))


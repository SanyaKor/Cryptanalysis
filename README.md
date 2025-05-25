## 📦 Dependencies

This project relies on external Python libraries listed in the `requirements.txt` file.  
To install them, use the following command:

```bash
pip install -r requirements.txt
```


📘 **Usage Examples:** See [notebooks/usage_examples.ipynb](notebooks/usage_examples.ipynb)  
for practical demonstrations of lattice reduction functions (`reduce_2d_basis`, `lll_reduce`, etc.).


### 📚 References

- **Trappe, W., & Washington, L. C.**  
  *Introduction to Cryptography with Coding Theory*, 2nd Edition. Pearson, 2006.

- **Hoffstein, J., Pipher, J., & Silverman, J. H.**  
  *NTRU: A Ring-Based Public Key Cryptosystem*, 1998.  
  [https://ntru.org](https://ntru.org)

- **Wikipedia**  
  *Lenstra–Lenstra–Lovász lattice basis reduction algorithm*  
  [Wikipedia article](https://en.wikipedia.org/wiki/Lenstra%E2%80%93Lenstra%E2%80%93Lov%C3%A1sz_lattice_basis_reduction_algorithm)

- **Tengely, Sz.**  
  *Public Key Cryptography – NTRU*  
  Example values and explanation used in this notebook are based on the example at:  
  [https://shrek.unideb.hu/~tengely/crypto/section-8.html](https://shrek.unideb.hu/~tengely/crypto/section-8.html)
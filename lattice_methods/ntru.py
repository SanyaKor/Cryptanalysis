"""
Implementation of the NTRU public-key cryptosystem.

Module author: Aleksandr Lebedev <alebede1@hs-mittweida.de>

This module provides functions for NTRU key generation, encryption, and decryption.
It offers efficient lattice-based cryptographic primitives aimed at post-quantum security,
supporting flexible parameter choices and secure message handling.
"""

from sympy import Poly, symbols, invert, ZZ, gcd, GF, isprime
import numpy as np

x = symbols('x')

def poly_inv_mod_ring(polynomial_f, N, q):
    """
    Computes the inverse of a polynomial modulo (pow(x,N) - 1) and q.

    This function attempts to find the inverse of a given polynomial `polynomial_f` in the ring
    of polynomials modulo (pow(x,N) - 1) with coefficients reduced modulo `q`. It works both when `q`
    is prime and composite by setting the appropriate polynomial domain.

    :param polynomial_f: The polynomial to invert (as a SymPy Poly object).
    :type polynomial_f: sympy.Poly
    :param N: The degree defining the modulus polynomial pow(x,N) - 1.
    :type N: int
    :param q: The modulus for coefficient arithmetic.
    :type q: int

    :return: List of coefficients of the inverse polynomial if it exists; otherwise, None.
    :rtype: list[int] or None

    .. note::
       The function returns None if `polynomial_f` is not invertible modulo (pow(x,N) - 1, q), i.e., if
       the gcd of `polynomial_f` and the modulus polynomial is not constant.
    """

    #f = Poly(f_coeffs, x, domain=GF(q))
    if(isprime(q)):
        mod_poly = Poly(x**N - 1, x, domain=GF(q))
    else:
        mod_poly = Poly(x ** N - 1, x, domain=ZZ).trunc(q)

    polynomial_f = polynomial_f.set_domain(mod_poly.domain)

    if gcd(polynomial_f, mod_poly).degree() != 0:
        return None

    try:
        inv = invert(polynomial_f, mod_poly)
        return inv.all_coeffs()
    except Exception:
        return None

def pad_left(poly, N):
    return [0] * (N - len(poly)) + poly


def poly_add_mod_ring(p1, p2, q):

    length = max(len(p1), len(p2))
    result = [0] * length

    p1 = pad_left(p1, length)
    p2 = pad_left(p2, length)

    for i in range(length):
        result[i] += (p1[i] + p2[i])

    return [c % q for c in result]

def poly_mult_mod_ring(p1, p2, N, q):
    """
    Performs multiplication of two polynomials modulo (pow(x,N) - 1) and coefficient modulus q.

    This function computes the product of two polynomials represented by coefficient lists `p1` and `p2`.
    The multiplication is done modulo the polynomial (pow(x,N) - 1), which means the coefficients
    are reduced with wrap-around at degree N, and all coefficients are taken modulo `q`.

    :param p1: Coefficients of the first polynomial (highest degree first).
    :type p1: list[int]
    :param p2: Coefficients of the second polynomial (highest degree first).
    :type p2: list[int]
    :param N: Degree of the modulus polynomial (pow(x,N) - 1).
    :type N: int
    :param q: Modulus for coefficient arithmetic.
    :type q: int

    :return: Coefficients of the resulting polynomial after modular multiplication,
             in highest degree first order.
    :rtype: list[int]

    .. note::
        The input polynomials are assumed to be represented as lists of coefficients with
        the highest degree coefficient first. The output is normalized to remove trailing zeros.
    """
    p1 = p1[::-1]
    p2 = p2[::-1]

    length = len(p1) + len(p2) - 1
    result = [0] * length
    for i in range(len(p1)):
        for j in range(len(p2)):
            idx = (i + j)
            result[idx] += p1[i] * p2[j]

    for i in range(len(result)):
        if(i > N-1):
            difference = i % N
            result[difference] += result[i]
            result[i] = 0

    for i in range(len(result)-1, -1, -1):
        if(result[i]!=0 or len(result) <= N):
            break

        result.pop(i)

    return [c % q for c in result[::-1]]

def check_coeff_range(poly_coeffs, bounds):
    """
    Checks whether all polynomial coefficients lie within specified bounds.

    This function verifies that each coefficient in `poly_coeffs` is within the inclusive range
    defined by `bounds` (left_bound and right_bound).

    :param poly_coeffs: List of polynomial coefficients.
    :type poly_coeffs: list[int]
    :param bounds: Tuple specifying inclusive lower and upper bounds (left_bound, right_bound).
    :type bounds: tuple[int, int]

    :return: True if all coefficients are within the bounds, False otherwise.
    :rtype: bool
    """
    left_bound, right_bound = bounds
    for i in range(len(poly_coeffs)):
        if(poly_coeffs[i] < left_bound  or poly_coeffs[i] > right_bound):
            return False

    return True

def center_poly_coeffs(poly, q):
    """
    Centers polynomial coefficients modulo q around zero.

    This function maps each coefficient `c` of the polynomial `poly` into the range
    [-q//2, q//2), effectively centering the coefficients modulo `q`.

    :param poly: List of polynomial coefficients.
    :type poly: list[int]
    :param q: Modulus for coefficient arithmetic.
    :type q: int

    :return: List of centered coefficients in the range [-q//2, q//2).
    :rtype: list[int]
    """
    return [((c + q//2) % q) - q//2 for c in poly]

def ntru_generate_keys(N : int, p: int, q : int, polynomial_g : Poly, polynomial_f : Poly):
    """
    Generates public and private keys for the NTRU cryptosystem.

    This function computes the NTRU key pair based on parameters N, p, q and the
    private polynomials `polynomial_f` and `polynomial_g`. It returns the public key
    and the inverse of `polynomial_f` modulo q, which serves as part of the private key.

    :param N: Degree of the polynomials and ring dimension.
    :type N: int
    :param p: Small modulus parameter for message space.
    :type p: int
    :param q: Large modulus parameter for polynomial arithmetic.
    :type q: int
    :param polynomial_g: Polynomial used in key generation (SymPy Poly).
    :type polynomial_g: sympy.Poly
    :param polynomial_f: Private polynomial used for key generation (SymPy Poly).
    :type polynomial_f: sympy.Poly

    :return: Tuple `(pub_key, prv_key)` where
         - `pub_key` is a list `[N, p, q, h]` representing the public key parameters and polynomial,
         - `prv_key` is a list `[polynomial_f, Fp]` representing the private key polynomial and its inverse modulo p.
    :rtype: tuple[list, list]
    """

    if(gcd(p, q) != 1 or p >= q):
        print("ERROR SMTH WRONG WITH p, q ")
        return

    if(isprime(q)):
        poly_f_over_q = Poly(polynomial_f, x, domain=GF(q))
    else:
        poly_f_over_q = Poly(polynomial_f, x, domain=ZZ).trunc(q)

    poly_f_over_p = Poly(polynomial_f, x, domain=GF(p))

    Fp = poly_inv_mod_ring(poly_f_over_p, N, p)
    Fq = poly_inv_mod_ring(poly_f_over_q, N, q)

    if Fp is None or Fq is None:
        print("ERROR SMTH WRONG WITH POLYNOMIALS Fq Fp")
        return

    Fqp = [p * x for x in Fq]
    h = poly_mult_mod_ring(Fqp, polynomial_g.all_coeffs(), N, q)

    pub_key = [N, p, q, h]
    prv_key = [polynomial_f, Fp]

    return pub_key, prv_key

def ntru_encryption(pubkey, polynomial_phi: Poly, polynomial_m: Poly):
    """
    Encrypts a message polynomial using the NTRU public key.

    This function performs NTRU encryption by computing the ciphertext polynomial as
    the sum of the product of the random polynomial `polynomial_phi` with the public key polynomial `h`,
    plus the message polynomial `polynomial_m`, all modulo `q`.

    :param pubkey: Public key represented as a list `[N, p, q, h]`.
    :type pubkey: list
    :param polynomial_phi: Random polynomial used for encryption (SymPy Poly).
    :type polynomial_phi: sympy.Poly
    :param polynomial_m: Message polynomial to encrypt (SymPy Poly).
    :type polynomial_m: sympy.Poly

    :return: Ciphertext polynomial coefficients modulo q.
    :rtype: list[int]
    """
    N, p, q, h = pubkey

    phi_coeffs = polynomial_phi.all_coeffs()
    m_coeffs = polynomial_m.all_coeffs()

    c = poly_mult_mod_ring(phi_coeffs, h, N, q)
    ciphertext = poly_add_mod_ring(c, m_coeffs, q)

    return ciphertext

def ntru_decryption(pubkey, prvkey, ciphertext):
    """
    Decrypts a ciphertext polynomial using the NTRU private key.

    This function performs NTRU decryption by multiplying the ciphertext with the private
    polynomial `polynomial_f` modulo (pow(x,N) - 1, q), centering the coefficients if needed,
    and then multiplying by the inverse of `polynomial_f` modulo p to recover the original message polynomial.

    :param pubkey: Public key represented as a list `[N, p, q, h]`.
    :type pubkey: list
    :param prvkey: Private key represented as a list `[polynomial_f, Fp]`,
                   where `polynomial_f` is the private polynomial and `Fp` its inverse modulo p.
    :type prvkey: list
    :param ciphertext: Ciphertext polynomial coefficients.
    :type ciphertext: list[int]

    :return: Decrypted message polynomial over GF(p).
    :rtype: sympy.Poly
    """
    [polynomial_f, Fp] = prvkey
    N, p, q, h = pubkey

    f_coeffs = polynomial_f.all_coeffs()
    a = poly_mult_mod_ring(f_coeffs, ciphertext, N, q)

    cond = check_coeff_range(a, (-q/2, q/2))
    if not cond:
        a = center_poly_coeffs(a, q)

    Fpa = poly_mult_mod_ring(Fp, a, N, p)
    #print(Poly(Fpa, x, domain=GF(p)))

    return Poly(Fpa, x, domain=GF(p))









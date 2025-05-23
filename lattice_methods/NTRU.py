from sympy import Poly, GF, symbols, gcd

x = symbols('x')

def is_invertible(f_coeffs, N, mod):

    R = GF(mod) ## galoes field READ
    f = Poly(f_coeffs, x, domain=R)
    mod_poly = Poly(x**N - 1, x, domain=R)
    return gcd(f, mod_poly).degree() == 0
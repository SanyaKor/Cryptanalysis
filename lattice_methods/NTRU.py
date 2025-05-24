from sympy import Poly, symbols, invert, ZZ, gcd, GF
import numpy as np
from typing import Tuple, List

x = symbols('x')


def invert_poly(polynomial_f, N, q):

    #f = Poly(f_coeffs, x, domain=GF(q))
    mod_poly = Poly(x**N - 1, x, domain=GF(q))

    if gcd(polynomial_f, mod_poly).degree() != 0:
        return None

    try:
        inv = invert(polynomial_f, mod_poly)
        return inv.all_coeffs()
    except Exception:
        return None

def pad_left(poly, N):
    return [0] * (N - len(poly)) + poly







# N = 5
# q = 16
# p = 3
# g = [1, 0, -1, 0]
# f = [1, 0, 0, 1, -1]
# N = 7
# p = 3
# q = 41
# phi = [1, -1, 0, 0, 0, 1, -1]
# m = [0, -1, 0, 1, 1, -1, 1]
# g = [1, 0, 1, 0, -1, -1, 0]
# f = [1, 0, -1, 1, 1, 0, -1]



#
#print(f"g = {Poly(g, x, domain=ZZ).trunc(q)} ")
# print(f"f = {Poly(f, x, domain=ZZ).trunc(q)} ")
#
# Fp = #invert_poly(f, N, p)
# Fq = #invert_poly(f, N, q)
# print(Fq)
# print(Fp)
# print(f"Fp = {Poly(Fp, x, domain=GF(p))}")
# print(f"Fq = {Poly(Fq, x, domain=GF(q))}")


#####################
#####################
#####################
#####################
#####################
#####################
#####################
#

# print(f"h = Fq * g = {Poly(h, x, domain=GF(q))}")
# #
# #
# # f = [9, 7, 1]    # 9 + 7x + x^2
# # g = [5, 2, 3]    # 5 + 2x + 3x^2
# # N = 3
# #
#
# print(f"Bobs public key: ({N}, {p}, {q}, {h} )")
# print(f"Bobs private key: ({f}) ")
# #
# #
# m = [1, -1, 1]
# phi = [1, -1]
# phi_scaled = [p * x for x in phi]
# #
# ciphertext = poly_mult_mod(phi_scaled, h, N, q)
# #
# m = pad_left(m, N)
# # # #
# c = [(ciphertext[i] + m[i]) % q for i in range(N)]
# print(f"c = 3 * phi * h + m = {Poly(c, x, domain=ZZ).trunc(q)}")
# # #
# # #
# print("------------")
# print("c(x):", c)
# print(Poly(c, x, domain=ZZ).trunc(q))
#
#
# # print("f:", f)
# #
# #
# a = poly_mult_mod(f, c, N, q)
# print(f"a = f * c= {Poly(a, x, domain=ZZ).trunc(q)}")
# res = poly_mult_mod(Fp, a,N, p)
# print(f"Fp * a = {Poly(res, x, domain=ZZ).trunc(q)}")


# coeffs = [1, 0, 1, 0, 2]  # x^4 + x^2 + 2
# N = 5
# p = 3

#canon = poly_mult_mod(coeffs, N, p)
#print("kek")
#print(canon)  # → x**2 - x + 1
# print(Fp)
# print(a)






def poly_mult_mod_strict(p1, p2, N, q):
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

# f = [1,7,9]         # x^6 ... x^0
# g = [3,2,5]     # x^6 ... x^0
# N = 3
# q = 2
#
# res = poly_mult_mod_strict(f, g,N,q)
# print("✅ Result:", res)
#
# print(Fq)
# Fqp = [p * x for x in Fq]
# print(Fqp)
#
# print("------------------")
# h = poly_mult_mod_strict(Fqp, g, N, q)
#
# print(f"ALL IN: {h}")
#
# print(f"h = {Poly(h, x, domain=GF(q))}")
#
#
#
# ciphertext = poly_mult_mod_strict(phi, h, N, q)
# c = [(ciphertext[i] + m[i]) % q for i in range(N)]
#
# print(c)
#
#
# a = poly_mult_mod_strict(f, c, N, q)
# print(f"a = f * c= {Poly(a, x, domain=GF(41))}")
#
#
# print(f"aaaaaaaaaaaa = {a}")


def check_coeff_range(poly_coeffs, bounds):
    left_bound, right_bound = bounds
    for i in range(len(poly_coeffs)):
        if(poly_coeffs[i] < left_bound  or poly_coeffs[i] > right_bound):
            return False

    return True



def to_centered_mod(poly, q):
    return [((c + q//2) % q) - q//2 for c in poly]

#
# print(check_coeff_range(a, (-q/2, q/2)))
# centered = to_centered_mod(a, q)
#
# print(check_coeff_range(centered, (-q/2 , q/2)))
# centered = to_centered_mod(a, q)
# #centered2 = to_centered_mod(Fp, p)
# print(f"centered = {centered}")
# centered = [c % p for c in centered]
# print(f"centered with mod= {centered}")
#
# rrrr = poly_mult_mod_strict(Fp, centered,N, p)
#
#
#
# print(f"Fp= {Poly(Fp, x, domain=GF(q))}")
# print(f"Fp * a= {Poly(rrrr, x, domain=GF(q))}")
# print(f"m = {Poly(m, x, domain=GF(p))}")


def ntru_generate_keys(N : int, p: int, q : int, polynomial_g : Poly, polynomial_f : Poly):

    if(gcd(p, q) != 1 or p >= q):
        print("ERROR SMTH WRONG WITH p, q ")
        return


    poly_f_over_q = Poly(polynomial_f, x, domain=GF(q))
    poly_f_over_p = Poly(polynomial_f, x, domain=GF(p))

    Fp = invert_poly(poly_f_over_p, N, p)
    Fq = invert_poly(poly_f_over_q, N, q)

    if Fp is None or Fq is None:
        print("ERROR SMTH WRONG WITH POLYNOMIALS Fq Fp")
        return

    Fqp = [p * x for x in Fq]
    h = poly_mult_mod_strict(Fqp, polynomial_g.all_coeffs(), N, q)

    pub_key = [N, p, q, h]
    prv_key = [polynomial_f, Fp]

    return pub_key, prv_key


def ntru_encryption(pubkey, polynomial_phi: Poly, polynomial_m: Poly):

    N, p, q, h = pubkey

    phi_coeffs = polynomial_phi.all_coeffs()
    m_coeffs = polynomial_m.all_coeffs()


    ##TODO ADDITION FOR POLYNOMIALS
    c = poly_mult_mod_strict(phi_coeffs, h, N, q)
    m_coeffs = pad_left(m_coeffs, N)

    ciphertext = [(c[i] + m_coeffs[i]) % q for i in range(N)]

    return ciphertext


def ntru_decryption(pubkey, prvkey, ciphertext):
    [polynomial_f, Fp] = prvkey
    N, p, q, h = pubkey

    f_coeffs = polynomial_f.all_coeffs()
    a = poly_mult_mod_strict(f_coeffs, ciphertext, N, q)

    cond = check_coeff_range(a, (-q/2, q/2))
    if not cond:
        a = to_centered_mod(a, q)

    Fpa = poly_mult_mod_strict(Fp, a, N, p)
    #print(Poly(Fpa, x, domain=GF(p)))

    return Poly(Fpa, x, domain=GF(p))


N = 7
p = 3
q = 41
phi = [1, -1, 0, 0, 0, 1, -1]
m = [0, -1, 0, 1, 1, -1, 1]
g = [1, 0, 1, 0, -1, -1, 0]
f = [1, 0, -1, 1, 1, 0, -1]




poly_f = Poly(f, x)
poly_g = Poly(g, x)
poly_m = Poly(m, x)
poly_phi = Poly(phi, x)

pub_key, prv_key = ntru_generate_keys(N, p, q, poly_g, poly_f)
ciphertext = ntru_encryption(pub_key, poly_phi, poly_m)
poly_d = ntru_decryption(pub_key, prv_key, ciphertext)

print(poly_m)
print (poly_d)








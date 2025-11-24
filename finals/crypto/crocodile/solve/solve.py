# Read Sections 2.1, 2.2 in Silverman's Rational Points on Elliptic Curves
# or solve Real Curve Crypto on Cryptohack first (<-- easier variant lol)
# This is an insane challenge. Do not worry if you weren't able to solve it during the CTF!

from sage.all import *

CC = ComplexField(600)
A, B = [ComplexField(600)(-1493709/1024+1199/16*ComplexField(600)("i")),ComplexField(600)(97809777/8192-82731/128*ComplexField(600)("i"))]
E = EllipticCurve(CC, [A, B])

G = E.lift_x(CC(f"1.{int.from_bytes(b'Suna Suna','big')}+1.{int.from_bytes(b'no Mi','little')}*i"))
Px = CC('36.4291990977855760916612664879030519474485549227993825161538502715951674771375534061669588110611144482794597140078219632113930698630358361379569599632450344672544557014134877316071 - 15.5094169179867261746136693539618921556037112420771075014010650669426508111314380331723075069743390329380360196986670381926994761597803212368978601671191064945527021806868498686789*I')
P = E.lift_x(Px)

# Get points of order 2
F = PolynomialRing(CC, name='x'); x = F.gens()[0]
f = x**3 + A*x + B
r0, r1, r2 = f.roots(multiplicities=False)
print(f"r0 = {r0.real().exact_rational()} + {r0.imag_part().exact_rational()}*I")
print(f"r1 = {r1.real().exact_rational()} + {r1.imag_part().exact_rational()}*I")
print(f"r2 = {r2.real().exact_rational()} + {r2.imag_part().exact_rational()}*I")

# Use weierstrass-inverse function to...
def weierstrass_p_inv(P):
    pari("\p 1000")
    pari(f"E = ellinit([{A}, {B}])")
    return CC(pari(f"ellpointtoz(E, [{P[0]}, {P[1]}])"))

# ...obtain lattice periods w1, w2, w1 + w2 (Told you to read Sections 2.1, 2.2!!)
z0, z1, z2 = \
    weierstrass_p_inv(E.lift_x(r0)) * 2, \
    weierstrass_p_inv(E.lift_x(r1)) * 2, \
    weierstrass_p_inv(E.lift_x(r2)) * 2
d0, d1, d2 = abs(z0+z1-z2), abs(z0+z2-z1), abs(-z0+z2+z1)
if d0 < min(d1, d2):
    w1, w2 = z0, z1
if d1 < min(d0, d2):
    w1, w2 = z0, z2
if d2 < min(d0, d1):
    w1, w2 = z1, z2
print(f'{w1 = }')
print(f'{w2 = }')

# So how we have vector invG, invP, and invG * FLAG == invP, modulo lattice periods
# we can model this as invG * FLAG + invP * -1 + w1 * k1 + w2 * k2 == 0
# split into real, imaginary coefficients (we can do this because imag, real are orthogonal wrt each other) 
# Solve for FLAG directly with LLL
rg, ig = weierstrass_p_inv(G).real(), weierstrass_p_inv(G).imag_part()
rp, ip = weierstrass_p_inv(P).real(), weierstrass_p_inv(P).imag_part()
w1r, w1i = w1.real(), w1.imag_part()
w2r, w2i = w2.real(), w2.imag_part()

M = Matrix(QQ, [[rg,ig,1,0],[rp,ip,0,1],[w1r,w1i,0,0],[w2r,w2i,0,0]])
ii = 38*8 # we know input length is probably around 38 bytes from print('\033[43C\033[1A}') --> 43 - len(b'sctf{') = 38
M[:,0] *= 4**ii
M[:,1] *= 4**ii
M[:,3] *= 2**ii
M = M.LLL()
for nrow in M:
    nrow[0] //= 4**ii
    nrow[1] //= 4**ii
    nrow[3] //= 2**ii
    nn = [round(i) for i in nrow]
    if nn[-1] == 1 or nn[-1] == -1:
        print(abs(nn[2]).to_bytes(38, "big"))
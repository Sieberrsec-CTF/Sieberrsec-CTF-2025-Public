from Crypto.Util.number import long_to_bytes
from pwn import *
import sys
sys.setrecursionlimit(10000)

# context.log_level = 'debug'

conn = process(["python", "h3math.py"])

mod = int(conn.recvline().split()[-1])
b = int(conn.recvline().split()[-1])

print("Getting leaks")

out1, out2 = None, None
for i in range(1000):
    conn.sendlineafter(b'flag:', b'1')
    conn.sendlineafter(b'point:', str(i).encode())
    temp = eval(conn.recvline())
    if(temp[1] < 16):
        out1 = temp
        break

for j in range(i+1, 1000):
    conn.sendlineafter(b'flag:', b'1')
    conn.sendlineafter(b'point:', str(j).encode())
    temp = eval(conn.recvline())
    if(temp[1] < 16):
        out2 = temp
        break

if(out1 is None or out2 is None):
    print("Unlucky, try running the script again!")
    exit()

R.<a> = Zmod(mod)[]

print("Forming polynomials")

eq1 = i
for i in range(out1[1]):
    eq1 = a * eq1 ** 2 + b
eq1 = eq1 - out1[0]

eq2 = j
for i in range(out2[1]):
    eq2 = a * eq2 ** 2 + b
eq2 = eq2 - out2[0]

def poly_gcd(a, b):
    if(b == 0):
        return a.monic()
    return poly_gcd(b, a % b)

print(f"Solving gcd with {out1[1]} and {out2[1]}")

a = int(mod - poly_gcd(eq1, eq2).coefficients()[0])

def gen(p):
    LEAK = 0
    while p.is_prime() == False or LEAK < 2:
        p = ((a*p**2 + int(b)) % mod)
        LEAK += 1
    return p

conn.sendlineafter(b'flag:', b'2')
N = int(conn.recvline()[4:])
e = int(conn.recvline()[4:])
c = int(conn.recvline()[4:])

p = gen(6969)

assert N % p == 0

q = N / p
phi = (q - 1) * (p - 1)
d = pow(e, -1, phi)

print(long_to_bytes(pow(c, d, N)))
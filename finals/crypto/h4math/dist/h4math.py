#!/usr/local/bin/python
from Crypto.Util.number import bytes_to_long, isPrime, getPrime
from Crypto.Random.random import getrandbits

with open('flag.txt', 'rb') as f:
    FLAG = f.read()

m = bytes_to_long(FLAG)
l = m.bit_length()
a, b = getPrime(l//2), getPrime(l//2)
mod = getPrime(l*3)
e = 0x10001

def gen(p):
    LEAK = 0
    while isPrime(p) == False or LEAK < 10:
        p = ((a*p**2 + b) % mod)
        LEAK += 1
    return p, LEAK

print(f'mod = {mod}')
print(f'b = {b}')
print('can you pass h4 math?????? play to find out!  ^w^ ^w^ ^w^')
while True:
    option = input('1. get a Super Secure private key, or 2. get encrypted flag:')
    if option == '1':
        seed = int(input('choose your starting point:')) % mod
        print(gen(seed))
    elif option == '2':
        x1, x2 = getrandbits(l), getrandbits(l)
        p, q = gen(x1), gen(x2)
        N = p[0] * q[0]
        c = pow(m, e, N)
        print(f'N = {N}')
        print(f'e = {e}')
        print(f'c = {c}')
        print(f'x1 = {x1}, x2 = {x2}')
        exit()


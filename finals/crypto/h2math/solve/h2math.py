#!/usr/local/bin/python
from Crypto.Util.number import bytes_to_long, isPrime, getPrime

with open('flag.txt', 'rb') as f:
    FLAG = f.read()

m = bytes_to_long(FLAG)
l = m.bit_length()
a = getPrime(l//2)
b = getPrime(l//2)
mod = getPrime(l*3)
e = 0x10001

def gen(p):
    LEAK = 0
    while isPrime(p) == False:
        p = ((a*p**2 + b) % mod)
        LEAK += 1
    return p, LEAK

print(f'mod = {mod}')
print('can you pass h2 math? play to find out!')
while True:
    option = input('1. get a Super Secure private key, or 2. get encrypted flag:')
    if option == '1':
        seed = int(input('choose your starting point:')) % mod
        if seed == 6767 or seed == 6969:
            print('no cheating >:/')
            exit()
        else:
            print(gen(seed))
    elif option == '2':
        p, q = gen(6767), gen(6969)
        N = p[0] * q[0]
        c = pow(m, e, N)
        print(f'N = {N}')
        print(f'e = {e}')
        print(f'c = {c}')
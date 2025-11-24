from Crypto.Util.number import long_to_bytes, isPrime
from pwn import *

# *** might need to run this a few times for it to work ***

# tldr: try small values of seed until LEAK (number of iterations) is 1

# get b by injecting 0
# notice there is no constraint on minimum bitlength of primes...
# go through small even numbers until LEAK == 1
# ^ this means prime produced is small, won't be affected by mod
# compute a
# reconstruct prng to get p, q. voila!


context.log_level = 'debug'

# conn = process(["python", "h2math.py"])
conn = remote('127.0.0.1', 9999)

mod = int(conn.recvline().split()[-1])
conn.recvline()
conn.sendlineafter(b'flag:', b'1')
conn.sendlineafter(b'point:', b'0')
b = eval(conn.recvline())[0]

for i in range(2, 500, 2):
    conn.sendlineafter(b'flag:', b'1')
    conn.sendlineafter(b'point:', str(i).encode())
    out = eval(conn.recvline())
    if int(out[1]) == 1:
        x = out[0]
        SEED = i
        break

conn.sendlineafter(b'flag:', b'2')
N = int(conn.recvline()[4:])
e = int(conn.recvline()[4:])
c = int(conn.recvline()[4:])
a = (x - b) // SEED**2
assert isPrime(a)

def gen(p):
    while isPrime(p) == False:
        p = ((a*p**2 + b) % mod)
    return p

p = gen(6767)
q = gen(6969)
print(p, q)
print(e)
phi = (p-1) * (q-1)
d = pow(e, -1, phi)

print(long_to_bytes(pow(c, d, N)))
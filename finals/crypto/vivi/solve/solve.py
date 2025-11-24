from struct import pack
from pwn import remote

def gf_mul(x, y):
    z = 0
    for i in range(128):
        if (y >> (127 - i)) & 1:
            z ^= x
        if x & 1:
            x = (x >> 1) ^ 0xe1000000000000000000000000000000
        else:
            x >>= 1
    return z

def gf_inv(a):
    a = int(format(a, f"0128b")[::-1], 2)

    # euclidean algo for inverse, but it works MSB to LSB. Hence the conversion above
    r0, r1 = 0x100000000000000000000000000000087, a
    s0, s1 = 0, 1

    while r1 != 0:

        # get quo-rem
        deg_r1 = r1.bit_length() - 1
        q, r, db = 0, r0, deg_r1
        while r.bit_length() - 1 >= db:
            shift = (r.bit_length() - 1) - db
            q ^= 1 << shift
            r ^= r1 << shift

        r0, r1 = r1, r

        # update bezout coeffs
        prod = 0
        for i in range(q.bit_length()):
            if (q >> i) & 1:
                prod ^= s1 << i
        while prod.bit_length() - 1 >= 128:
            shift = (prod.bit_length() - 1) - 128
            prod ^= 0x100000000000000000000000000000087 << shift

        s0, s1 = s1, s0 ^ prod

    assert r0 == 1 # else no inv exists
    return int(format(s0, f"0128b")[::-1], 2)


r = remote('127.0.0.1',20001)

# keystream, keytag = enc_gcm(b"\x00" * 32)
r.recvuntil(b'>> ')
r.sendline(b'1')
r.sendline(b'0' * 64)
r.recvuntil(b"ct:")
keystream = bytes.fromhex(r.recvline().rstrip().decode())
r.recvuntil(b"tag:")
keytag = bytes.fromhex(r.recvline().rstrip().decode())

# rec_iv = dec_ecb(keystream)[:12]
r.recvuntil(b'>> ')
r.sendline(b'3')
r.sendline(keystream.hex().encode())
r.recvuntil(b"pt:")
rec_iv = bytes.fromhex(r.recvline().rstrip().decode())[:12]
print(f'{rec_iv = }')

# H = enc_ecb(b'\x00'*16)
r.recvuntil(b'>> ')
r.sendline(b'2')
r.sendline(b'0' * 32)
r.recvuntil(b"ct:")
H = bytes.fromhex(r.recvline().rstrip().decode())
H = int.from_bytes(H,'big')
Hinv = gf_inv(H)

# J0 = enc_ecb(rec_iv + b'\x00\x00\x00\x01')
r.recvuntil(b'>> ')
r.sendline(b'2')
r.sendline(rec_iv.hex().encode() + b"00000001")
r.recvuntil(b"ct:")
J0 = bytes.fromhex(r.recvline().rstrip().decode())

htag = int.from_bytes(bytes([i^j for i,j in zip(keytag, J0)]), 'big')
bitlens = int.from_bytes(pack('>QQ', 8 * 8, 32 * 8), 'big')
htag = gf_mul(htag, Hinv) ^ bitlens
htag = gf_mul(htag, Hinv) ^ int.from_bytes(keystream[16:], 'big')
htag = gf_mul(htag, Hinv) ^ int.from_bytes(keystream[:16], 'big')
htag = gf_mul(htag, Hinv)
rec_aad = htag.to_bytes(16, 'big')[:8]
print(f'{rec_aad = }')

def ghash(H, A, C):
    X = 0
    for block in [A + b'\x00' * 8] + [C[i:i+16] for i in range(0, len(C), 16)]:
        X = gf_mul(X ^ int.from_bytes(block, "big"), H)
    bitlens = pack('>QQ', len(A) * 8, len(C) * 8)
    X = gf_mul(X ^ int.from_bytes(bitlens, "big"), H)
    return X.to_bytes(16, 'big')

r.recvuntil(b'>> ')
r.sendline(b'5')
r.recvuntil(b'Challenge:')
challenge = bytes.fromhex(r.recvline().rstrip().decode())
# challenge = random.randbytes(32)
# correct_ct, correct_tag = enc_gcm(challenge)
my_ct = bytes([i^j for i,j in zip(challenge, keystream)])
my_tag = bytes([i^j for i,j in zip(ghash(H, rec_aad, my_ct), J0)])
# assert my_ct == correct_ct and my_tag == correct_tag
# print(verify(my_ct, my_tag) == challenge)

r.sendline(my_ct.hex().encode())
r.sendline(my_tag.hex().encode())
print(r.recvline())
r.close()
"""
[x] Opening connection to 127.0.0.1 on port 20001
[x] Opening connection to 127.0.0.1 on port 20001: Trying 127.0.0.1
[+] Opening connection to 127.0.0.1 on port 20001: Done
rec_iv = b'11\x1e@l\x86\xf1\xc2\xf91\xc9`'
rec_aad = b'\xe3\x8a=\xfd\x0c<k\xb1'
b">> >> b'sctf{n0w_1_knoW_how_a3s_gCM_bar0qu3-work5!}'\n"
[*] Closed connection to 127.0.0.1 port 20001
"""
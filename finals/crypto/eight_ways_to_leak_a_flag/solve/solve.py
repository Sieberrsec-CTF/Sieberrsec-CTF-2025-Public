from nacl.bindings import crypto_scalarmult
import hashlib

with open("../dist/out.txt", "rb") as f:
    ciphertext = f.read()

pub_key = bytes.fromhex("e0eb7a7cbf2c8e51a8d0f17ec8e6d47461f7b2d16cfa2b6b1d45b4f1c9ff0f00")
scalars = [bytes([i] + [0]*31) for i in range(1, 9)]

for i, scalar in enumerate(scalars, 1):
    shared = crypto_scalarmult(scalar, pub_key)
    key = hashlib.sha256(shared).digest()
    plaintext = bytes([c ^ k for c, k in zip(ciphertext, key[:len(ciphertext)])])
    print(f"[{i}] {plaintext}")
    if b"sctf" in plaintext:
        print(plaintext.decode())
from nacl.bindings import crypto_scalarmult
import hashlib

with open("flag.txt", "rb") as f:
    flag = f.read()

priv_bytes = bytes([8] + [0]*31)
pub_key = bytes.fromhex("e0eb7a7cbf2c8e51a8d0f17ec8e6d47461f7b2d16cfa2b6b1d45b4f1c9ff0f00")
shared = crypto_scalarmult(priv_bytes, pub_key)
key = hashlib.sha256(shared).digest()
ciphertext = bytes([f ^ k for f, k in zip(flag, key[:len(flag)])])

with open("out.txt", "wb") as f:
    f.write(ciphertext)
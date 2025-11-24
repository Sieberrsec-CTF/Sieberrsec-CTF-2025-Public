import os

def xor(data: bytes, key: bytes) -> bytes:
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

with open("flag.txt", "rb") as f:
    flag = f.read().strip()

key = os.urandom(5)
encrypted = xor(flag, key)

with open("out.txt", "wb") as f:
    f.write(encrypted)
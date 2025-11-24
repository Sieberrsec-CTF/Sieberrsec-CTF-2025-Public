import os
from Crypto.Cipher import AES

KEY = os.urandom(16)
NONCE = os.urandom(8)
with open("flag.txt", "rb") as f:
    FLAG = f.read().strip()

KNOWN = [
    b"balls",
    b"balls the",
    b"balls the flag",
    b"balls the flag is",
    b"balls the flag is gullible",
    b"balls the flag is gullible balls",
    b"balls the flag is gullible balls balls",
    b"balls the flag is gullible balls balls balls",
    b"balls the flag is gullible balls balls balls balls",
    b"balls the flag is gullible balls balls balls balls balls",
    b"balls the flag is gullible balls balls balls balls balls balls",
    b"balls the flag is gullible balls balls balls balls balls balls balls",
    b"balls the flag is gullible balls balls balls balls balls balls balls balls",
    b"balls the flag is gullible balls balls balls balls balls balls balls balls balls",
    b"balls the flag is gullible balls balls balls balls balls balls balls balls balls balls",
    b"balls the flag is gullible balls balls balls balls balls balls balls balls balls balls balls",
    b"balls the flag is gullible balls balls balls balls balls balls balls balls balls balls balls balls",
    b"balls the flag is gullible balls balls balls balls balls balls balls balls balls balls balls balls balls",
    b"balls the flag is gullible balls balls balls balls balls balls balls balls balls balls balls balls balls balls",
    b"balls the flag is gullible balls balls balls balls balls balls balls balls balls balls balls balls balls balls balls",
    b"balls the flag is gullible balls balls balls balls balls balls balls balls balls balls balls balls balls balls",
    b"balls the flag is gullible balls balls balls balls balls balls balls balls balls balls balls balls balls",
    b"balls the flag is gullible balls balls balls balls balls balls balls balls balls balls balls balls",
    b"balls the flag is gullible balls balls balls balls balls balls balls balls balls balls balls",
    b"balls the flag is gullible balls balls balls balls balls balls balls balls balls balls",
    b"balls the flag is gullible balls balls balls balls balls balls balls balls balls",
    b"balls the flag is gullible balls balls balls balls balls balls balls balls",
    b"balls the flag is gullible balls balls balls balls balls balls balls",
    b"balls the flag is gullible balls balls balls balls balls balls",
    b"balls the flag is gullible balls balls balls balls balls",
    b"balls the flag is gullible balls balls balls balls",
    b"balls the flag is gullible balls balls balls",
    b"balls the flag is gullible balls balls",
    b"balls the flag is gullible balls",
    b"balls the flag is gullible",
    b"balls the flag is",
    b"balls the flag",
    b"balls the",
    b"balls"
]

def encrypt(data):
    cipher = AES.new(KEY, AES.MODE_CTR, nonce=NONCE)
    return cipher.encrypt(data)

with open("out.txt", "w") as f:
    enc_flag = encrypt(FLAG)
    f.write(f"enc = {enc_flag.hex()}\n\n")
    for pt in KNOWN:
        ct = encrypt(pt)
        f.write(f"{ct.hex()}\n")
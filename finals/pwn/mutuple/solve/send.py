from pwn import *
from base64 import b64encode

p = remote("localhost", 5000)

with open("./solve.py", "rb") as file:
    payload = b64encode(file.read())
    p.sendlineafter(b">", payload)

p.interactive()

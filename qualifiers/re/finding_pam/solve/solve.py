from pwn import *

context.log_level = 'error'

mapping = {}
for i in range(33, 127):
    char = chr(i)
    p = process('./chall')
    p.recvuntil(b': ')
    p.sendline(bytes(char.encode()))
    num = p.recvline().strip().decode()
    mapping[num] = char

# enc is obtained from decompiling the binary
enc = "1012 3602 1497 7985 5115 9749 1861 9263 9328 1861 5134 9328 7149 2203 5404 1250 9328 7149 7004 9046 5404 9749 7149 2203 9920 6819 7149 3400 7149 9263 3400 2651 7653"
print(''.join([mapping[x] for x in enc.split()]))

from pwn import *

elf = context.binary = ELF('../src/intro')

# io = remote('chal1.sieberr.live', 10002)
io = elf.process(stdin=PTY)


for i in range(50):
    # get n1
    io.recvuntil(b'n1: ')
    n1 = int(io.recvline())
    # get n2
    io.recvuntil(b'n2: ')
    n2 = int(io.recvline())

    print(n1,n2)
    output = n1 * n2

    # send n1 * n2
    io.sendline(str(output))

io.interactive()

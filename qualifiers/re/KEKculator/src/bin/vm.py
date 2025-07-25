#!/usr/local/bin/python3
'''
32 bit cpu  
writes are done by converting the number/whatever into hex and then writing 1 byte by 1byte to the memory block --> where the potential overflow comes into play
big endian

registers stored in list [esp, ebp, eip, eax(used for arithmetic calls) ,edx, ecx, ebx, esi, edi]
memory block [
    0:1000 -> stack
    1001: -> code
]

opcode format
4 bytes (opcode), 4 bytes (arg 1), 4 bytes (arg 2), 4 bytes (arg 3)

all integers are unsigned 

opcodes:
0x00 -> halt (arg1 = exit_code, arg2 = message, arg3 = 0)
0x01 -> add (arg1 = dest(register), arg2 = src1, arg3 = src2)
0x02 -> sub (arg1 = dest(register), arg2 = src1, arg3 = src2)
0x03 -> mul (arg1 = dest(register), arg2 = src1, arg3 = src2)
0x04 -> div (arg1 = dest(register), arg2 = src1, arg3 = src2)
0x05 -> test (arg1 = src1, arg2 = src2, arg3 = 0) -> clears the flags of register tes
0x06 -> jeq (arg1 = offset, arg2 = 0, arg3 = 0) -> jumps if the eq is set (tested equality)
0x07 -> jne (arg1 = offset, arg2 = 0, arg3 = 0) -> jumps if the neq flag is not set (tested inequality)
0x08 -> jgt (arg1 = offset, arg2 = 0, arg3 = 0) -> jumps if the greater than flag is set (tested greater than)
0x09 -> jlt (arg1 = offset, arg2 = 0, arg3 = 0) -> jumps if the less than flag is set (tested less than)
0x0a -> jz (arg1 = offset, arg2 = 0, arg3 = 0) -> jumps if the zero  flag is set (tested equality)
0x0b -> jnz (arg1 = offset, arg2 = 0, arg3 = 0) -> jumps if the zero flag is not set (tested inequality)
0x0c -> jmp (arg1 = offset, arg2 = 0, arg3 = 0) -> jumps unconditionally
0x0d -> push (arg1 = dest(register), arg2 = value)
0x0e -> pop (arg1 = dest(register), arg2 = 0)
0xff -> nop (arg1 = 0, arg2 = 0, arg3 = 0) -> no operation
0xdd -> syscall (arg1(0=print, 1=read), arg2(resgiter), arg3(register))
when an opcode is met, the next 12 bytes (4*3) are popped into the registers arg1, arg2 and arg3 to be used as arguments

'''

'''
simple calculator app that lets you basically call sub, mul, div, add

however, none of the writes actually do bounds checking, so you can simply calculate a bigass integer, which when written to somewhere on the stack, will end up overflowing into the code range giving you rce
'''

import sys

class VM:
    def __init__(self, code):
        # [esp, ebp, eip, eax(used for arithmetic calls) ,edx, ecx, ebx, esi, edi]
        self.registers = {
            'esp': 0, 'ebp': 0, 'eip': 0, 'eax': 0, 'edx': 0, 'ecx': 0, 'ebx': 0, 'esi': 0, 'edi': 0, 'arg1': 0, 'arg2': 0, 'arg3': 0
        }        
        self.registers['eip'] = 1000
        self.memory = [0] * (1000 + len(code))
        self.memory[1000:] = code
    def __exit(self):
        exit('Error occured...program exiting')
    
    def __get_string(self, address):
        '''
        gets bytes from address=address untill a null byte is met
        cleanly exits program if OOB write is attempted
        '''
        output = ''
        if address > len(self.memory):
            self.__exit()
        else:
            while self.memory[address] != 0:
                output = output + chr(self.memory[address])
                address += 1
                if address > len(self.memory):
                    self.__exit()
                    
        return output
    
    def __get_register(self, value):
        register_names = ['esp', 'ebp', 'eip', 'eax', 'edx', 'ecx', 'ebx', 'esi', 'edi', 'arg1', 'arg2', 'arg3']
        regs = [6648688, 6644336, 6646128, 6644088, 6644856, 6644600, 6644344, 6648681, 6644841, 1634887473, 1634887474, 1634887475]
        if value in regs:
            return register_names[regs.index(value)]

        else:
            self.__exit()
    
    def __halt(self):
        '''
        halts the program and finishes execution
        if arg2 is set, it will print the value of the string @ memory address arg2 until a null byte is encountered
        if arg2 is not set, it will print the exit code arg1
        '''
        
        # print('eip is at: ', self.registers['eip'])
        # case where arg2 is not set
        if self.registers['arg2'] == 0:
            exit(f'Program exited with exit code {self.registers["arg1"]}')
            
        else:
            string = self.__get_string(self.registers['arg2'])
            exit(string)
            
    def __add(self):
        '''
        adds arg2 and arg3 (registers) and stores the result into arg1 (register)
        arg1 = arg2 + arg3
        '''
        
        # gets the values to be added
        a = self.registers['arg2']
        b = self.registers['arg3']
        
        # check if the values inputted are registers
        # this sadly means that none of these values can be used in any arithmetic expression! :o
        if a in [6648688, 6644336, 6646128, 6644088, 6644856, 6644600, 6644344, 6648681, 6644841, 1634887473, 1634887474, 1634887475]:
            a = self.registers[self.__get_register(a)]
        
        if b in [6648688, 6644336, 6646128, 6644088, 6644856, 6644600, 6644344, 6648681, 6644841, 1634887473, 1634887474, 1634887475]:
            b = self.registers[self.__get_register(b)]
        
        # destination register
        dest = self.__get_register(self.registers['arg1'])
        self.registers[dest] = a + b
        
    def __sub(self):
        '''
        subtracts arg2 and arg3 (registers) and stores the result into arg1 (register)
        arg1 = arg2 - arg3
        '''
        
        # gets values to be subbed
        a = self.registers['arg2']
        b = self.registers['arg3']
        
        # check if the values inputted are registers
        # this sadly means that none of these values can be used in any arithmetic expression! :o
        if a in [6648688, 6644336, 6646128, 6644088, 6644856, 6644600, 6644344, 6648681, 6644841, 1634887473, 1634887474, 1634887475]:
            a = self.registers[self.__get_register(a)]
        
        if b in [6648688, 6644336, 6646128, 6644088, 6644856, 6644600, 6644344, 6648681, 6644841, 1634887473, 1634887474, 1634887475]:
            b = self.registers[self.__get_register(b)]
        
        # destination register
        dest = self.__get_register(self.registers['arg1'])
        
        self.registers[dest] = abs(a - b)
        
    def __mul(self):
        '''
        multiplies arg2 and arg3 (registers) and stores the result into arg1 (also register)
        arg1 = arg2 * arg3
        '''
        
        # gets the values to be added
        a = self.registers['arg2']
        b = self.registers['arg3']
        
        # check if the values inputted are registers
        # this sadly means that none of these values can be used in any arithmetic expression! :o
        if a in [6648688, 6644336, 6646128, 6644088, 6644856, 6644600, 6644344, 6648681, 6644841, 1634887473, 1634887474, 1634887475]:
            a = self.registers[self.__get_register(a)]
        
        if b in [6648688, 6644336, 6646128, 6644088, 6644856, 6644600, 6644344, 6648681, 6644841, 1634887473, 1634887474, 1634887475]:
            b = self.registers[self.__get_register(b)]
        
        # destination register
        dest = self.__get_register(self.registers['arg1'])
        # print(f'multiplying')
        self.registers[dest] = a * b
        # print([hex(i) for i in self.memory[0x938:0x938+32]])
        
    def __div(self):
        '''
        divides arg2 and arg3 (registers) and stores the result into arg1 (also register)
        floors the the number as this cpu only stores integers (oops)
        arg1 = arg2 * arg3
        '''
        
        # gets the values to be added
        a = self.registers['arg2']
        b = self.registers['arg3']
        
        # check if the values inputted are registers
        # this sadly means that none of these values can be used in any arithmetic expression! :o
        if a in [6648688, 6644336, 6646128, 6644088, 6644856, 6644600, 6644344, 6648681, 6644841, 1634887473, 1634887474, 1634887475]:
            a = self.registers[self.__get_register(a)]
        
        if b in [6648688, 6644336, 6646128, 6644088, 6644856, 6644600, 6644344, 6648681, 6644841, 1634887473, 1634887474, 1634887475]:
            b = self.registers[self.__get_register(b)]
        
        # check for /0 error
        if b == 0:
            self.__exit()
        
        # destination register
        dest = self.__get_register(self.registers['arg1'])
        
        self.registers[dest] = a // b
        
    
    def __test(self):
        ''' 
        test instruction for arg1 and arg2 (registers), stores the result as a number into eax
        00000001 if arg1 == arg2
        00000010 if arg1 != arg2
        00000100 if arg1 > arg2
        00001000 if arg1 < arg2
        
        0s out eax then does the comparison
        '''
        self.registers['eax'] = 0
        
        # gets the values needed for the comparison
        a = self.registers[self.__get_register(self.registers['arg1'])]
        b = self.registers[self.__get_register(self.registers['arg2'])]
        
        value = 0
        
        # set the bits for the equality comparison
        if a == b:
            value = value + 1
        else:
            value = value + 2
            # set the bits for the gt and lt checks
            
            if a > b:
                value = value + 4
            
            else:
                value = value + 8
                
        self.registers['eax'] = value
        
    def __jeq(self):
        ''' 
        arg1 address
        jump to code @ arg1 if eax & 1 != 0
        '''
        # print('jumping if equal to ', self.registers['arg1'])
        if self.registers['eax'] & 0b1:
            self.registers['eip'] = self.registers['arg1'] - 16  # -32 because it will be incremented at the end of the loop
        
    def __jz(self):
        '''
        effectively does the same thing as __jeq
        '''
        
        self.__jeq() 
        
    def __jne(self):
        ''' 
        arg1 address
        jump to code @ arg1 if eax & 0b10 != 0
        '''
        
        if self.registers['eax'] & 0b10:
            self.registers['eip'] = self.registers['arg1'] - 16  # -4 because it will be incremented at the end of the loop
            
    def __jnz(self):
        self.__jne()
        
    def __jgt(self):
        ''' 
        arg1 address
        jump to code @ arg1 if eax & 0b100 != 0
        '''
        
        if self.registers['eax'] & 0b100:
            self.registers['eip'] = self.registers['arg1'] - 16  # -4 because it will be incremented at the end of the loop
            
    def __jlt(self):
        ''' 
        arg1 address
        jump to code @ arg1 if eax & 0b1000 != 0
        '''
        
        if self.registers['eax'] & 0b1000:
            self.registers['eip'] = self.registers['arg1'] - 16  # -4 because it will be incremented at the end of the loop
            
    def __jmp(self):
        '''
        arg1 address
        jump to code @ arg1
        '''
        
        self.registers['eip'] = self.registers['arg1'] - 16
        
        
    def __push(self):
        '''
        pushes arg1(register) onto the stack
        '''
        
        value = self.registers[self.__get_register(self.registers['arg1'])]
        bits = value.bit_length()
        byte_count = (bits + 8 - 1) // 8
        added_count = 0
        if bits % 32 < 25:
            extra_bytes = 4 - ( (bits + 8 - 1) // 8 ) % 4 # i hope this is correct?
            for i in range(extra_bytes):
                self.memory[self.registers['esp']+added_count] = 0x00
                added_count += 1
        for i in range(byte_count, 0, -1):
            # get byte to add
            b = (value >> (8 * (i-1))) & 0xff
            # print(hex(b))
            self.memory[self.registers['esp'] + added_count] = b
            added_count = added_count + 1
        
        # increment the stack pointer by 4 (pushed a 4 byte value)
        # if self.registers['eip'] == 0x938+16:
            # print('esp is now: ', self.registers['esp'])
        self.registers['esp'] += 4
        
    def __pop(self):
        '''
        pops a 4 byte number off the stack into arg1
        '''
        reg = self.__get_register(self.registers['arg1'])
        # get lower to upper bytes
        b1 = self.memory[self.registers['esp']-1]
        b2 = self.memory[self.registers['esp']-2]
        b3 = self.memory[self.registers['esp']-3]
        b4 = self.memory[self.registers['esp']-4]
        
        value = (b1) + (b2 << 8) + (b3 << 16) + (b4 << 24)
        self.registers[reg] = value
        self.registers['esp']  = self.registers['esp'] - 4     
    
    
    
    def __syscall(self):
        '''
        arg1 --> syscall type (0=print, 1=read, 2=open)
            print:
                arg2 -> register that points to memory address of string to print
            
            read:
                arg2 -> register to store read value in (will only read first 4 bytes of user input, ignores the rest)
                
            
            open:
                arg2 -> register that points to a string referencing the file to read
                arg3 -> register to store the value to 
        '''
        syscall = self.registers['arg1']
        # print('syscall', syscall)
        if syscall not in [0,1,2]:
            self.__exit()
            
        if syscall == 0:
            addr = self.registers[self.__get_register(self.registers['arg2'])]
            # print(hex(addr))
            string = self.__get_string(addr)
            print(string)
            
        elif syscall == 1:
            value = sys.stdin.buffer.readline()[:4]
            # print('input value', str(value))
            value = int(value.hex(),16)
            # store the value in
            self.registers[self.__get_register(self.registers['arg2'])] = value
        
        else:
            string_addr = self.registers[self.__get_register(self.registers['arg2'])]
            filename = self.__get_string(string_addr)
            # print(f'string_addr: ', string_addr)
            reg_store = self.__get_register(self.registers['arg3'])
            
            value = open(filename).read()
            # print('value:', value, 'stored in register', reg_store)
            value = int(value.encode().hex(),16)
            
            self.registers[reg_store] = value
    
    def __store(self):
        '''
        stores arg1(register) into arg2(memory (stores unconditionally) (used for strings!))
        arg1 -> src(register) 
        arg2 -> memory addr
        '''
        
        value = self.registers[self.__get_register(self.registers['arg1'])]
        addr = self.registers['arg2']
        value = value.to_bytes((value.bit_length()+7)//8)
        # print(len(self.memory))
        # print('storing value of len', len(value))
        for b in value:
            self.memory[addr] = b
            addr = addr + 1
        # print('last addr', hex(addr))
        # print('eip:', hex(self.registers['eip']+16))
        # print([hex(i) for i in self.memory[0x9ca:0x9ca+16]])
        
    def __nop(self):
        pass


    def __get_four_bytes(self, start):
        b1 = self.memory[start+3]
        b2 = self.memory[start+2]
        b3 = self.memory[start+1]
        b4 = self.memory[start]
        value = (b1) + (b2 << 8) + (b3 << 16) + (b4 << 24)
        return value
        
    def start(self):
        ''' 
        registers stored in list [esp, ebp, eip, eax(used for arithmetic calls) ,edx, ecx, ebx, esi, edi]
        memory block [
            0:1000 -> stack
            1001: -> code
        ]
        
        when this point has been hit, the program will read 32 bytes from eip: opcode, arg1, arg2, arg3 (this also helps to clear the previous arguments)
        call the function for the opcode
        increment the eip by 32(next instruction, this has been considered in the jmp functions as well already)
        runs in a while loop, program execution will pause on an __exit or __halt call
        0x00 -> halt 
        0x01 -> add
        0x02 -> sub
        0x03 -> mul
        0x04 -> div
        0x05 -> test 
        0x06 -> jeq 
        0x07 -> jne 
        0x08 -> jgt 
        0x09 -> jlt 
        0x0a -> jz 
        0x0b -> jnz 
        0x0c -> jmp 
        0x0d -> push 
        0x0e -> pop 
        0xff -> nop 
        0xdd -> syscall
        '''
        
        while True:
            eip = self.registers['eip']
            
            opcode = self.__get_four_bytes(eip)
            self.registers['arg1'] = self.__get_four_bytes(eip+4)
            self.registers['arg2'] = self.__get_four_bytes(eip+8)
            self.registers['arg3'] = self.__get_four_bytes(eip+12)
            # match opcode:
            #     case 0x00:
            #         self.__halt()
                
            #     case 0x01:
            #         self.__add()
                    
            #     case 0x02:
            #         self.__sub()
                    
            #     case 0x03:
            #         self.__mul()
                    
            #     case 0x04:
            #         self.__div()
                    
            #     case 0x05:
            #         self.__test()
                    
            #     case 0x06:
            #         self.__jeq()
                    
            #     case 0x07:
            #         self.__jne()
                    
            #     case 0x08:
            #         self.__jgt()
                    
            #     case 0x09:
            #         self.__jlt()
                    
            #     case 0x0a:
            #         self.__jz()
                    
            #     case 0x0b:
            #         self.__jnz()
                    
            #     case 0x0c:
            #         self.__jmp()
                    
            #     case 0x0d:
            #         self.__push()
                    
            #     case 0x0e:
            #         self.__pop()
                    
            #     case 0x0f:
            #         self.__store()
                    
            #     case 0xff:
            #         self.__nop()
                    
            #     case 0xdd:
            #         self.__syscall()
            
            if opcode == 0x00:
                self.__halt()

            elif opcode == 0x01:
                self.__add()

            elif opcode == 0x02:
                self.__sub()

            elif opcode == 0x03:
                self.__mul()

            elif opcode == 0x04:
                self.__div()

            elif opcode == 0x05:
                self.__test()

            elif opcode == 0x06:
                self.__jeq()

            elif opcode == 0x07:
                self.__jne()

            elif opcode == 0x08:
                self.__jgt()

            elif opcode == 0x09:
                self.__jlt()

            elif opcode == 0x0a:
                self.__jz()

            elif opcode == 0x0b:
                self.__jnz()

            elif opcode == 0x0c:
                self.__jmp()

            elif opcode == 0x0d:
                self.__push()

            elif opcode == 0x0e:
                self.__pop()

            elif opcode == 0x0f:
                self.__store()

            elif opcode == 0xff:
                self.__nop()

            elif opcode == 0xdd:
                self.__syscall()
                
            self.registers['eip'] += 16
with open('bytecode.bin', 'rb') as f:
    code = f.read()
env = VM(code)

env.start()
        
            
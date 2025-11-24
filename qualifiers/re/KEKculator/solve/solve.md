overwrite needs to be @ memory index 0x9c8 (next eip will be)

writes to 0x74 onward
therefore we need a 0x954 long write

our exploit will look like the following

<0x8c4 bytes of anything that doesn't start with 0>
<shellcode>
0x0000000c000009380000000000000000 (jmp innstruction)


shellcode (in bytes)

0000000100656378666c6167000000000000000d00656378000000000000000000000001006563780000000000000000000000dd0000000200656378006562780000000f00656278000001000000000000000001006562780000010000000000000000dd00000000006562780000000000000000000000000000000000000000
say first 16 bytes are 0x10000000000000000000000000000000



first we need to find a chain of operations that allows us to get 0x8c4 bytes of numbers
0x8c4 bytes is 0x4620 (17952) bits,
of course, to minimize operations we must naturally use big numbers

```
>>> hex(0xffffffff*0xffffffff)
'0xfffffffe00000001'
```


this basically does a bitshift left of 31 bits, so we can just keep repeating this bitshift till we find something that satisfies
```
>>> (0xffffffff**561).bit_length()
25952
```

after some manual searching, we find we will need ( 561) operations to achieve this

ps:
```
sys.set_int_max_str_digits(9999999)
```
might be useful at this juncture

now, we calculate the offset of our shellcode which is 0x74 + 0x8c4 = 0x938
therefore, at the end of shellcode, we need to add a jmp 0x938 0x0 0x0 instruction

now we will perform our arbitrary write as follows
split our payload into 3 byte chunks -> total 144 bytes, so a perfect 48 chunks total

(the reason we don't use 4 byte chunks here is that you can't get a bitshift left by 4 bytes with just a 4 byte mutltiplication as 0xffffffff is 255 and not 256! [i made this mistake when conceiving this solution at first])


there after we need to repeat this loop 144 times 
for the Nth interation, bitshift left by 3 bytes (mul, 0x1000000)
add the 3 bytes of our payload to the current value (add, CHUNK)


afterwhich, we can simply send the "DONE" instruction and win!
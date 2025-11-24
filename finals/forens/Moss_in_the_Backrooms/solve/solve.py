with open(r"Moss_in_the_Backrooms.jpg", "rb") as f:
    infile = f.read()

flag = [i >> 7 for i in infile] # Get leftmost bit of each byte
flag = [str(i) for i in flag] # Convert each bit string for easier processing
flag = ['0b'+''.join(flag[i:i+8]) for i in range(0, 8*len(flag)//8, 8)] # Recreate bytes from bits
flag = [chr(int(i, 0)) for i in flag] # Convert bytes to string
# print(''.join(flag)) # Would not work, as the backspaces after the flag would be printed as well and "hide" the flag
print(''.join(flag[:flag.index("}")+1])) # Stop printing before the backspaces start
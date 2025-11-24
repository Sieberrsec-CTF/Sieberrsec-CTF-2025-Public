import sys
print(sys.argv)
string_to_print = sys.argv[1]

# print(string_to_print.encode())
a = string_to_print
words = [a[i*4:(i+1)*4].encode().hex() for i in range((len(a)+3)//4)]


for word in words:
    print(f'add edx 0x{word} 0x0')
    print('push edx 0x0 0x0')
    

import sys
a = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ"+ \
            "[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~ "
def check_password(password):
  if password == 'happychance':
    return True
  else:
    print('That password is incorrect')
    sys.exit(0)
    return False
def arg111(arg444):
  return arg122(arg444.decode(), 'rapscallion')
def get_user_input():
  return input('Please enter correct password for flag: ')
def read_flag_bytes():
  return open('flag.txt.enc', 'rb').read()
def display():
  print('Welcome back... your flag, user:')
def arg122(arg432, arg423):
    arg433 = arg423
    i = 0
    while len(arg433) < len(arg432):
        arg433 = arg433 + arg423[i]
        i = (i + 1) % len(arg423)        
    return "".join([chr(ord(arg422) ^ ord(arg442)) for (arg422,arg442) in zip(arg432,arg433)])
flag_bytes_enc = read_flag_bytes()
user_input = get_user_input()
check_password(user_input)
display()
arg423 = arg111(flag_bytes_enc)
print(arg423)
sys.exit(0)


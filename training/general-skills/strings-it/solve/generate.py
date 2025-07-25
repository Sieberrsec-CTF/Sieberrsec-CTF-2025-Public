import random
import string

NUM_VARS = 10000
MIN_LEN = 15     
MAX_LEN = 50     

output = ''

for i in range(NUM_VARS):
    var_name = f"s{i}"
    str_len = random.randint(MIN_LEN, MAX_LEN)
    rand_str = ''.join(random.choices(string.ascii_letters + string.digits, k=str_len))
    output += f'char {var_name}[] = "{rand_str}";\n'

with open('random.txt','w') as f:
    f.write(output)
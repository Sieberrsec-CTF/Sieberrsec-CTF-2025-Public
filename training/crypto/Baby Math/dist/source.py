from Crypto.Util.number import bytes_to_long, getPrime
from random import randrange

# flag has 39 characters
flag = 'sctf{redacted}'
flag_num = bytes_to_long(flag.encode())

divisors = [getPrime(randrange(5, 30)) for _ in range(17)]
remainders = [flag_num % divisor for divisor in divisors]

print(f"{divisors = }")
print(f"{remainders = }")

# Output:
# divisors = [439429297, 107, 60586153, 509311637, 56196341, 587, 1061, 3096757, 59, 193, 3637, 130003, 37243, 1148339, 254899, 15140887, 1904537]
# remainders = [319989397, 11, 3768949, 192286989, 6160298, 584, 830, 550668, 32, 181, 2842, 90486, 2658, 608727, 237542, 13861648, 862306]
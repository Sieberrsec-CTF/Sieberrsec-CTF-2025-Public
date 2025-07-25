from secret import flag
from random import randrange
from Crypto.Util.number import bytes_to_long

assert len(flag) == 48

# split flag into parts of length 8
flag_parts = [flag[idx:idx+8] for idx in range(0, len(flag), 8)]

n = 2 ** 400 # we will perform matrix multiplications under modulo n

# calculate number of flag parts
k = len(flag) // 8

# defining a 1 x k row vector A. unfortunately i forgot what it was :(
A = [bytes_to_long(flag_part.encode('UTF-8')) for flag_part in flag_parts]

# my homework worksheet matrix is k x (k - 2) with random values
B = [[randrange(n) for _ in range(k - 2)] for __ in range(k)]

# doing my homework! calculating C = A * B, a 1 x (k - 2) row vector
C = [sum([A[idx] * B[idx][idx2] for idx in range(k)]) % n for idx2 in range(k - 2)]

print(f"{B = }")
print(f"{C = }")
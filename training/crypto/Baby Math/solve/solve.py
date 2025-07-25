from Crypto.Util.number import long_to_bytes
def crt_implementation(divisors, remainders):
    product = 1
    for divisor in divisors:
        product *= divisor

    ans = 0
    for divisor, remainder in zip(divisors, remainders):
        ans += (product // divisor) * pow(product // divisor, -1, divisor) * remainder
        ans %= product
    
    for divisor, remainder in zip(divisors, remainders):
        assert ans % divisor == remainder
    
    return ans, product

divisors = [439429297, 107, 60586153, 509311637, 56196341, 587, 1061, 3096757, 59, 193, 3637, 130003, 37243, 1148339, 254899, 15140887, 1904537]
remainders = [319989397, 11, 3768949, 192286989, 6160298, 584, 830, 550668, 32, 181, 2842, 90486, 2658, 608727, 237542, 13861648, 862306]

rem, modulo = crt_implementation(divisors, remainders)

for cand in range(rem, 2 ** 312, modulo):
    cand_flag = long_to_bytes(cand)
    if cand_flag[:4] == b'sctf':
        print(cand_flag.decode())
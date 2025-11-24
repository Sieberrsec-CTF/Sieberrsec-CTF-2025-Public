from output import B, C
from sage.all import *
from Crypto.Util.number import long_to_bytes

k = 48 // 8
table = [[0 for _ in range(k + 2)] for __ in range(k + 2)]

for i in range(0, k):
    table[i][0] = B[i][0]
    table[i][i + 1] = 1

heavy = 2 ** 200

table[-1][0] = -C[0]
table[-1][-1] = heavy ** 3

table[-2][0] = 2 ** 400

for row in table:
    for idx in range(len(row)):
        if not idx:
            row[idx] *= heavy

A = matrix(ZZ, table)
B = A.LLL()

for row in B:
    # print(row)
    if row[0] == 0 and row[-1] == heavy ** 3:
        ans = ''
        for num in row[1:-1]:
            ans += long_to_bytes(num).decode()
        print(ans)
from output import B, C, secret_hash
from sage.all import *
import itertools
from tqdm import tqdm
from hashlib import sha256

n = 131
k = 21

known_positions = {
    0: ord('s'),
    1: ord('c'),
    2: ord('t'),
    3: ord('f'),
    4: ord('{'),
    k - 1: ord('}')
}

sanity_check = ['0', '1', '2', '3']
cand = range(5, k - 1)

F = GF(131)
errors = set()

first_B = None
first_C = None

for combi in tqdm(list(itertools.product(cand, cand, cand, cand))):
    if len(set(combi)) != len(sanity_check):
        continue
    tmp = known_positions.copy()
    for pos, char in zip(combi, sanity_check):
        tmp[pos] = ord(char)
    C_tmp = C.copy()
    for idx in range(len(C_tmp)):
        for pos in tmp:
            C_tmp[idx] -= tmp[pos] * B[pos][idx]
        C_tmp[idx] %= n
    B_tmp = [
        B[idx].copy() for idx in range(len(B)) if not idx in tmp
    ]

    B_mat = matrix(F, B_tmp)
    C_mat = matrix(F, [C_tmp])
    if first_B is None:
        first_B, first_C = B_mat.list(), C_mat.list()


    B_rows, B_cols = B_mat.nrows(), B_mat.ncols()
    C_rows, C_cols = C_mat.nrows(), C_mat.ncols()

    try:
        A_mat = B_mat.solve_left(C_mat)
        A = A_mat[0]
        ans = ''
        idx = 0
        for i in range(k):
            if i in tmp:
                ans += chr(tmp[i])
            else:
                ans += chr(int(A[idx]))
                idx += 1
        ans_hash = sha256(ans.encode('utf-8')).hexdigest()
        if ans_hash == secret_hash:
            print(ans)
            break

    except Exception as e:
        errors.add(str(e))
        continue

print("=" * 30 + "Errors" + "=" * 30)
for e in errors:
    print(e)
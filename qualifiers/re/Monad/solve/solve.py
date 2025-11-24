enc = "v,Khe\)mX[nmX*i\KXl\A9mt[m_l\\"

enc = [*enc][::-1]

for i in range(0, len(enc) // 2):
    enc[i * 2], enc[i * 2 + 1] = enc[i * 2 + 1], enc[i * 2]

flag = "".join(chr(ord(c) + 7) for c in enc)

print(flag)
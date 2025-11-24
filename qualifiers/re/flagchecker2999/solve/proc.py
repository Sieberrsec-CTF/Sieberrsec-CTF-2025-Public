flag = "sctf{El3m3n74ry_fl46_ch3cker_8031265d}"
realkey = 0x67

enc = []

for c in flag:
    enc.append(ord(c) ^ realkey)

print(enc)
print(len(enc))
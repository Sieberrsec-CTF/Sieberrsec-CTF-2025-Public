import random

sub = [i for i in range(256)]
random.shuffle(sub)

print(sub)

with open("matryoshka.jpg", "rb") as file:
    flag = file.read()

enc = []
for i in flag:
    enc.append(sub.index(i))

with open("enc", "w") as file:
    file.write(", ".join([str(i) for i in enc]))

for i in range(8):
    print(sub[enc[i]], end = " ")

print()
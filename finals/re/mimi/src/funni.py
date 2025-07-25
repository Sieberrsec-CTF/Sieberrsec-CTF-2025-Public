# sol="chzbchzczchzczbezezezeqvvbeqezcqcqbezbeqczbcqvbezczehzbvezezvczeqezcqcqcqbvvvezczeqcqbehzvvvbeqvbcqchzbvvvezbcqcqcqbezvvezezehqcqchzeqvbezezbcqbezezbvczehqcqchzezezvvezbcqcqbezezeqezehqcqchzezezbcqchzezezehqbezehqbehqbehhhhhq"

# ls = []
# for i in range(0, len(sol)):
#     if sol[i] == 'b':
#         ls.append(i)
# print(ls[0])
# for j in range(1, len(ls)):
#     print(ls[j] - ls[j-1], end=', ')


xkey = [i % 256 for i in [75, 74, 179, 64, 170, 144, 102, 204, 72, 131, 230, 243, 53, 220, 37, 107, 157, 163, 205, 160, 6, 177, 157, 174, 143, 117, 210, 123, 25, 188, 108, 73, 167, 145, 167, 208, 195, 128, 0, 73, 103, 44, 225, 85, 99, 34]]
print([i ^ j for i,j in zip(xkey, b"[sctf{s1mpl3...l0oozzzzzzzzzzzzzzzzzzzzzzzzz}]")])


# import random
# xx = open("aaa.cpp",'rb').read()
# for ii in range(15):
#     while f"{ii}000".encode() in xx:
#         ptr = xx.index(f"{ii}000".encode())
#         num = ii*1000 + random.randint(0, 1000)
#         xx = xx[:ptr] + str(num).encode() + xx[ptr+4:]
# open("bbb.cpp","wb").write(xx)
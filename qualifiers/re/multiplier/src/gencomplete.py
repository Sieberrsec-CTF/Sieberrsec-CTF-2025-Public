import random
import os
import time


sequence = random.sample(range(99999999), 10)
sequence = [78519025] + sequence

print(sequence)

for i in range(1, len(sequence)):

    sub = [j for j in range(256)]   
    random.shuffle(sub)
    
    print(f"packing file {sequence[i]}")
    print(f"reading file {sequence[i-1]}")
    with open(f"factory/wrapper{sequence[i-1]}", "rb") as file:
        chall = file.read()

    enc = []
    for k in chall:
        enc.append(sub.index(k))

    with open(f"factory/wrapper{sequence[i]}.c", "w") as file:
        print(f"writing to file {sequence[i]}")
        file.write(f"""#include <stdio.h>
#include <stdlib.h>

int key[] = {{  {", ".join([str(j) for j in sub])}  }};
int enc[] = {{  {", ".join([str(j) for j in enc])}  }};
int main() {{
    FILE *fptr;
    fptr = fopen("child{sequence[i-1]}", "w");
    int length = sizeof(enc) / sizeof(enc[0]);
    unsigned char dec;

    for (int i = 0; i < length; i++) {{
        dec = key[enc[i]];
        fprintf(fptr, "%c", dec);
    }}

    fclose(fptr);

    system("chmod +x child{sequence[i-1]}");
    system("./child{sequence[i-1]}");
    system("rm child{sequence[i-1]}");
}}""")

    print("compiling...")
    os.system(f"gcc factory/wrapper{sequence[i]}.c -o factory/wrapper{sequence[i]}")
    os.system(f"upx --best factory/wrapper{sequence[i]}")

    
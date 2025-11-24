import random

flag = "sctf{h0p3_y0u_d1d_n07_bru73_f0rc3_7h15_bb36204c84}"

start = """
#include <stdio.h>

int main()
{
    char flag[50];
    printf("enter the flag: ");
    scanf("%s", &flag);
    
    bool valid = 1;
    int value = 0;
"""


end = """
    if (valid) {
        printf("valid flag! \\n");
    }
    else {
        printf("invalid flag! \\n");
    }

    return 0;
}
"""

output = start

for c in flag:
    print(ord(c), end=" ")
print()
for i in range(50):
    exps = []
    value = 0
    for j in range(50):
        coeff = random.randint(-50, 50)
        exps.append(f"(flag[{j}] * {coeff})")
        value += coeff * ord(flag[j])
    
    exp = " + ".join(exps)
    output += f"\tif (({exp}) != {value})\n"
    output += f"\t{{valid = 0;}}\n\n"

output += end

with open("chall.c", "w") as file:
    file.write(output)
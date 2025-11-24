#include <stdio.h>


int main()
{
    char flag[38];
    printf("enter the flag: ");
    scanf("%s", &flag);

    unsigned char enc[] = {20, 4, 19, 1, 28, 34, 11, 84, 10, 84, 9, 80, 83, 21, 30, 56, 1, 11, 83, 81, 56, 4, 15, 84, 4, 12, 2, 21, 56, 95, 87, 84, 86, 85, 81, 82, 3, 26};
    
    bool valid = 1;
    for (int i = 0; i < sizeof(enc); i++) {
        if ((enc[i] ^ 0x67) != flag[i]) {
            valid = 0;
        }
    }

    if (valid) {
        printf("valid flag! \n");
    }
    else {
        printf("invalid flag! \n");
    }

    return 0;
}
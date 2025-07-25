#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int tries = 1;

void init(){
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
}
    
void secret(){
    if(tries == 0) return;
    tries--;
    uint64_t addr = 0;
    scanf("%lu", &addr);
    printf("%lx\n", *(int64_t *)addr);
}

int main(){
    init();
    uint64_t choice;
    char buffer[0x10];

    while(1){
        printf("What would you like to do?\n");
        printf("1) Try BOF\n");
        printf("2) Try again\n");
        printf("3) Give up\n");
        scanf("%lu", &choice);
        getchar();
        switch(choice){
            case 1:
                fgets(buffer, sizeof(buffer) + 0x70, stdin);
                break;
            case 2:
                main();
                break;
            case 3:
                return 0;
            case 0x1337:
                secret();
                break;
            default:
                printf("Invalid input: %lu\n", choice);
        }
    }
}
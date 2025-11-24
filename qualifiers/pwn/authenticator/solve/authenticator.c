#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <fcntl.h>

#define PWD_SIZE 0x10

void authenticate(char *password){
    char buffer[PWD_SIZE];
    
    printf("Please enter your current password: ");
    read(0, buffer, sizeof(buffer));

    if(memcmp(buffer, password, PWD_SIZE)){
        printf("Intruder detected!\n");
        exit(0);
    }

    printf("Welcome, admin\n>> ");
    read(0, buffer, 0x100);
}

void reset_password(char *password){
    char buffer[0x100];

    printf("Please enter your current password: ");
    int read_chars = read(0, buffer, sizeof(buffer));

    if(memcmp(buffer, password, read_chars)){
        printf("Incorrect password!\n");
        return;
    }

    printf("Unfortunately, this feature isn't implemented yet.\n");
}

void menu(){
    printf("1) Authenticate\n");
    printf("2) Reset password\n");
    printf("3) Exit\n");
    printf("What would you like to do?\n");
}

void init(char *password){
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);

    int fd = open("/dev/urandom", O_RDONLY);
    int read_chars = read(fd, password, PWD_SIZE);

    if(read_chars != PWD_SIZE){
        printf("Something went wrong! Open a ticket.\n");
        exit(0);
    }
}

int main(){
    char password[PWD_SIZE];
    int input;

    init(password);

    while(1){
        menu();
        scanf("%d", &input);
        getchar();

        switch(input){
            case 1:
                authenticate(password);
                break;
            case 2:
                reset_password(password);
                break;
            case 3:
                return 0;
            default:
                printf("Invalid input!\n");
        }
    }
}
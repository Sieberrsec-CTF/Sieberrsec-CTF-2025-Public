// gcc -o main main.c -no-pie
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char WELCOME_MSG[] = "Welcome to SecureLogin 3000™";
char GOODBYE_MSG[] = "Thank you for using SecureLogin 3000™";

int logged_in = 0;

void login()
{
    char username[100];
    FILE *log = fopen("/dev/null", "a"); // real log

    printf("Enter your username: ");
    fgets(username, sizeof(username), stdin);
    username[strcspn(username, "\n")] = 0;

    if (strcmp(username, "skibidiadmin123") == 0)
    {
        puts("Access granted.");
        logged_in = 1;
    }
    else
    {
        puts("Access denied, suspicious activity will be logged!");
        fprintf(log, username);
    }

    fclose(log);
}

void gurt(char *yo)
{
    system(yo);
}

int main()
{
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    puts(WELCOME_MSG);

    while (1)
    {
        printf("\n1. Login\n2. Exit\n3. Admin Panel\n> ");
        int choice;
        scanf("%d", &choice);
        getchar();

        switch (choice)
        {
        case 1:
            login();
            break;
        case 2:
            puts(GOODBYE_MSG);
            exit(0);
            break;
        case 3:
            if (logged_in)
            {
                puts("Welcome admin! The flag is sctf{fake_flag_really_fake}");
            }
            else
            {
                puts("Not authenticated");
            }
            break;
        default:
            puts("Invalid choice.");
        }
    }

    return 0;
}
/*
Compile options:
    gcc intro.c -o intro
*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void print_flag()
{   
    system("cat flag.txt");
}

int calculate() 
{   
    setbuf(stdin, 0);
    setbuf(stdout, 0);
    setbuf(stderr, 0);
    
    int n1 = rand()%1000;
    int n2 = rand()%1000;
    int input;

    printf("n1: %d\n",n1);
    printf("n2: %d\n",n2);

    printf("What is the value when n1 is multiplied by n2? ");

    // invalid input
    if(scanf("%d", &input) == 0) {
        puts("Invalid input, please input an integer next time.");

        int ch;
        do {
            ch = getchar();
        } while ((ch != EOF) && (ch != '\n'));
        return 0;
    }

    // check if input is correct
    if(input == (n1*n2)) {
        return 1;
    }

    return 0;
}

int main() 
{   
    int score = 0;
    puts("Welcome to the introduction to pwntools exercise!");
    puts("In this exercise, your goal is to earn a total of 50 points.\n");

    puts("We will be providing you with 2 numbers, and you should use pwntools and python to multiply the 2 numbers together.");
    puts("A correct answer will garner you 1 point.");

    srand(time(0));

    while (score < 50) {
        if (calculate()!=1) {
            puts("That is incorrect");
        }
        else {
            puts("That is correct");
            score += 1;
        }
        printf("Your score: %d\n\n",score);
    }

    if (score == 50) {
        print_flag();
    }

    return 0;
}
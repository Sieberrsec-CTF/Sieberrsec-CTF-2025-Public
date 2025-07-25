#include <stdio.h>
#include <stdlib.h>

#define SWORD_DAMAGE 10
#define POTION_HEAL 15
#define MONSTER_DAMAGE 15
#define PLAYER_INITIAL_HEALTH 50
#define MONSTER_INITIAL_HEALTH 80

void print_status(char player_hp, char monster_hp, char turn) {
    printf("\n--- Turn %d ---\n", turn);
    printf("Your HP: %d\n", player_hp);
    printf("Monster HP: %d\n", monster_hp);
    printf("---------------------------------------\n\n");
}

void print_welcome() {
    printf("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠤⣤⣤⣀⡀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢧⢸⣄⠉⠁⠉⢉⡲⢤\n"
    "⠀⠀⠀⢀⡠⠴⠊⣭⠃⠀⣀⣀⡤⠴⢶⠤⠤⢤⣀⠀⢸⠸⠈⠣⡀⢠⠃⠀⠀\n"
    "⠀⢀⢔⡉⢀⣀⠐⠐⢧⣾⣴⣿⡿⠀⠀⡏⡄⠀⠀⢱⡧⢀⡠⠤⠬⣎⣧⠀⠀\n"
    "⠐⠋⠁⠀⠀⢸⠔⢢⣿⣿⣿⡿⠃⠀⢠⠃⠀⠠⢚⣉⣠⢯⠀⠀⠀⠈⠛⠀⠀\n"
    "⠀⠀⠀⠀⠀⠈⠀⣼⠙⠛⠉⠀⢀⣠⢊⠆⠀⠀⠈⣴⠃⣼⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⡌⢦⣀⣀⠬⡺⠕⠁⠀⠀⠀⢀⠟⠸⡟⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⡇⣀⠀⡦⢄⣠⣾⣿⣾⣦⠀⢀⠼⢱⠁⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠳⡏⠉⠁⣀⠈⠻⣿⣿⠉⠀⠈⢠⠇⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⡏⠁⠈⠙⣿⢟⡀⢀⠄⢹⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⣀⡤⠀⡤⠃⠫⡉⠙⠃⠁⠀⠈⠠⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠰⠐⡀⠀⠀⠀⠀⣨⠆⠀⣀⠤⠒⠀⠙⠣⠤⠐⠒⠒⠄⡀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⢀⡤⠒⠊⡉⠀⠀⡜⠄⠀⠘⣏⡄⠀⣀⡠⠤⠠⢄⠘⡄⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⢸⠀⡔⣳⠒⠒⠚⣿⠀⠰⢎⠀⠈⠁⠀⠀⠀⠀⢠⠇⡼⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠈⠳⢌⡘⢄⡀⠀⠘⠦⣀⣉⣉⣁⠒⣄⠀⠀⠀⣸⢼⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣈⡧⣸⠀⠀⠀⠀⢠⠔⠋⢀⡼⠀⠀⠀⠉⠉⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠓⠊⠁⠀⠀⠀⠀⠈⠙⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠠⠤⠠⠤⠴⠠⠠⠠⠤⠤⠀⠠⠲⠀⠆⠤⠦⠴⠰⠀⠀⠀⠀\n");
    printf("Welcome to the Dungeon\n");
    printf("=======================================\n");
    printf("Brave warrior, there is a monster in the way of your exit.\n");
    printf("Fight the monster valiantly. If you succeed, you will be honoured with a flag.\n");
    printf("=======================================\n\n");
}

int main() {

    setbuf(stdin, 0);
    setbuf(stdout, 0);
    setbuf(stderr, 0);

    char player_hp = PLAYER_INITIAL_HEALTH;
    char monster_hp = MONSTER_INITIAL_HEALTH;
    char turn = 1;
    
    print_welcome();

    while (1) {
        print_status(player_hp, monster_hp, turn);

        // Player's turn
        printf("Choose an action:\n");
        printf("1. Use sword (-10 health)\n");
        printf("2. Use healing potion (+15 health)\n");
        printf("3. Give up\n");
        printf("> ");

        int choice;
        if (scanf("%d", &choice) != 1) {
            printf("Invalid input!\n");
            exit(1);
        }

        if (choice == 3) {
            printf("You gave up! What a cowardly warrior...\n");
            exit(0);
        }

        printf("Target:\n");
        printf("1. Yourself\n");
        printf("2. Monster\n");
        printf("> ");

        int target;
        if (scanf("%d", &target) != 1 || (target != 1 && target != 2)) {
            printf("Invalid target!\n");
            exit(1);
        }

        if (choice == 1) {
            if (target == 1) {
                printf("You stabbed yourself with the sword... why did you do that... -10 HP.\n");
                player_hp -= SWORD_DAMAGE;
            } else {
                printf("You hit the monster! -10 HP to the monster.\n");
                monster_hp -= SWORD_DAMAGE;
            }
        } else if (choice == 2) {
            if (target == 1) {
                printf("You used a healing potion on yourself. +15 HP.\n");
                player_hp += POTION_HEAL;
            } else {
                printf("You healed the monster... why did you do that... +15 HP to the monster.\n");
                monster_hp += POTION_HEAL;
            }
        } else {
            printf("Invalid action!\n");
            exit(1);
        }

        // Check if monster is defeated
        if (monster_hp <= 0) {
            printf("You defeated the monster! Victory!\n");
            printf("Here is your reward, valiant warrior: \n");
            system("cat flag.txt");
            exit(0);
        }

        // Monster's turn
        printf("The monster attacks you! -15 HP.\n");
        player_hp -= MONSTER_DAMAGE;

        // Check if player is dead
        if (player_hp <= 0) {
            printf("You died! Game over.\n");
            exit(0);
        }

        turn++;
    }

    return 0;
}

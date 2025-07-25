// gcc chall.c -o chall -no-pie -fno-stack-protector

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int sanitize_path(char *input) {
    int len = strlen(input);
    // Check for empty string
    if (len == 0) {
        printf("Error: Empty path not allowed\n");
        return 0;
    }
    // Check maximum length
    if (len > 255) {
        printf("Error: Path too long (max 255 characters)\n");
        return 0;
    }
    // Check each character
    for (int i = 0; i < len; i++) {
        char c = input[i];
		if (c == '\'') {
            printf("Error: Path cannot contain '\n");
			return 0;
		}
    }
    // Check for dangerous substrings
    if (strstr(input, "//") != NULL) {
        printf("Error: Double slashes '//' not allowed\n");
        return 0;
    }
    return 1;
}

int main() {
	setbuf(stdin, 0);
	setbuf(stdout, 0);

    char final_cmd[0x1000] = "export PATH='";
    char input[256];
    int choice;
    while (1) {
        printf("\n=== Environment Variable Menu ===\n");
        printf("1. Add another environment variable\n");
        printf("2. Reset environment variable\n");
        printf("3. Print environment variable so far\n");
        printf("4. Save and finish\n");
        printf("Enter your choice: ");
        if (scanf("%d", &choice) != 1) {
            printf("Invalid input. Please enter a number.\n");
            while (getchar() != '\n'); // Clear input buffer
            continue;
        }
        switch (choice) {
            case 1:
                printf("Enter path to add: ");
                while (getchar() != '\n'); // Clear input buffer
                if (fgets(input, sizeof(input), stdin) != NULL) {
                    // Remove newline if present
                    input[strcspn(input, "\n")] = 0;
					
					if (!sanitize_path(input)) {
						break;
					}

					// Add colon separator if not the first entry after the opening quote
					if (strlen(final_cmd) > strlen("export PATH='")) {
						strcat(final_cmd, ":");
					}
					strcat(final_cmd, input);
					printf("Added: %s\n", input);
				}
				break;
            case 2:
				strcpy(final_cmd, "export PATH='");
				printf("Environment variable is now empty.\n");
                break;
            case 3:
                printf("Current command: %s'\n", final_cmd);
                break;
            case 4:
                // Close the quote and execute
                strcat(final_cmd, "'");
                printf("Executing: %s\n", final_cmd);
                system(final_cmd);
				return 0;
            default:
                printf("Invalid choice. Please select 1, 2, or 3.\n");
                break;
        }
    }
    return 0;
}

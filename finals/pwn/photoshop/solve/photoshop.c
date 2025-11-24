#include <stdio.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>
#include <stdlib.h>

#define IMAGE_SIZE 0x100000

char *image;

int main(){
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    printf("Welcome to the best image editing software!\n");
    printf("Loading image...\n");
    sleep(3);

    image = mmap((void *)0x10000, IMAGE_SIZE, PROT_NONE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);

    int fd = open("./icon.png", O_RDONLY);
    mprotect(image, IMAGE_SIZE, (PROT_READ|PROT_WRITE) & 7);
    int read_chars = read(fd, image, IMAGE_SIZE);

    if(read_chars < 0){
        printf("Something went wrong! Open a ticket.\n");
        exit(0);
    }

    int value = 0, index = 0;
    char buffer[0x10];

    printf("You can edit one pixel!\n");
    printf("Enter in the index you want to edit: ");

    scanf("%u", &index);

    if(index >= IMAGE_SIZE || index < 0){
        printf("Invalid!\n");
        return 0;
    }

    printf("Enter in the value: ");
    scanf("%d", &value);

    image[index] = (char)value;

    printf("Edit successful!\n");
    printf("Saving image...\n");
    sleep(3);

    mprotect(image, IMAGE_SIZE, ~(PROT_WRITE) & 7);

    printf("Enter in a review? ");
    read(0, buffer, 0x108);
}
// gcc main.c -o main -Ofast -no-pie -Wl,-z,relro -Wl,-z,now -s
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

typedef struct {
    unsigned int size;
    char name[8];
    char data[];
} Order;

#define MAX_ORDERS 4

Order *orders[MAX_ORDERS];

void create_order() {
    int idx;
    for (idx = 0; idx < MAX_ORDERS; idx++) {
        if (!orders[idx])
            break;
    }

    if (idx == MAX_ORDERS) {
        puts("All slots full.");
        return;
    }

    unsigned int size, order_size;
    printf("Size of order: ");
    scanf("%u", &size);
    getchar();

    order_size = sizeof(Order) + size;

    if (size == 0) {
        puts("Invalid size!");
        return;
    }

    if (order_size > 0x400) {
        puts("Order too big!");
        return;
    }

    Order *order = malloc(order_size);
    if (!order) {
        puts("Alloc failed");
        return;
    }
    order->size = size;

    printf("Your name: ");
    ssize_t len = read(0, order->name, sizeof(order->name) - 1);
    if (len > 0) order->name[len] = '\0';
    else order->name[0] = '\0';

    printf("Your order: ");
    len = read(0, order->data, order->size - 1);
    if (len > 0) order->data[len] = '\0';
    else order->data[0] = '\0';

    orders[idx] = order;
    printf("Order created at index %d\n", idx);
}

void view_order() {
    int idx;
    printf("Index: ");
    scanf("%d", &idx);
    getchar();

    if (idx < 0 || idx >= MAX_ORDERS || !orders[idx]) {
        puts("Invalid index.");
        return;
    }

    printf("\nName: %s", orders[idx]->name);
    printf("Order: %s", orders[idx]->data);
}

void update_order() {
    int idx;
    printf("Index: ");
    scanf("%d", &idx);
    getchar();

    if (idx < 0 || idx >= MAX_ORDERS || !orders[idx]) {
        puts("Invalid index.");
        return;
    }
    Order* order = orders[idx];

    printf("New content: ");
    ssize_t len = read(0, order->data, order->size - 1);
    if (len > 0) order->data[len] = '\0';
    else order->data[0] = '\0';

    puts("Order updated.");
}

void delete_order() {
    int idx;
    printf("Index: ");
    scanf("%d", &idx);
    getchar();

    if (idx < 0 || idx >= MAX_ORDERS || !orders[idx]) {
        puts("Invalid index.");
        return;
    }

    free(orders[idx]);
    orders[idx] = NULL;
    puts("Order cancelled.");
}

int main() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
    
    puts("Welcome to McDonald's may I take your order?");

    int c;
    while (1) {
        puts("1) New Order");
        puts("2) View Order");
        puts("3) Update Order");
        puts("4) Cancel Order");
        puts("5) Leave");
        printf("> ");
        if (scanf("%d", &c) != 1)
            break;
        getchar();

        switch (c) {
            case 1:
                create_order();
                break;
            case 2:
                view_order();
                break;
            case 3:
                update_order();
                break;
            case 4:
                delete_order();
                break;
            case 5:
                puts("bye");
                exit(0);
            default:
                puts("Invalid option.");
        }
        puts("");
    }
    return 0;
}

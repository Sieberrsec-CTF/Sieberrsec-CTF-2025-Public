#include <stdio.h>

// r14 -> pointer to constructor array
// r12 -> pointer to argv

int __attribute__((naked)) __attribute__((constructor)) func1() {
	__asm__(
		"sub r14, 8\n" // we want to find a way to hide this
		"ret\n"
	);
}
int main() {
	puts("hello world");
}

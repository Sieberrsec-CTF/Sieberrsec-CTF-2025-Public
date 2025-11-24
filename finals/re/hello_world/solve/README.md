# Explaining the Obfuscation

This program code is hidden within the constructor of the program.

In the constructor, we run chunk this assembly code

```asm
frame_dummy:
	endbr64
	xchg rsp, r14
	sub rsp, 8
	pop rax
	add rax, strip_make_rwx_memory-frame_dummy
	push rax
	xchg rsp, r14
    jmp register_tm_clones # this is benign
```

This modifies the non volatile register, effectively doing 

```
sub r14, 8
mov [r14], offset_to_strip_make_rwx_memory
```

The `__libc_start_main` function uses the `r14` function to store the pointer to the constructor array.

We are effectively modifying the address of the constructor function and setting the pointer to the next snippet of shellcode that we are going to run.

We can trace this easily by doing `break *__libc_start_main+249` where it will call the next constructor in the array.

# Tracing the assembly

1. mprotect to make .text section RWX
2. XOR decrypt more shellcode
3. check argc == 2
4. check strlen(argv[1]) == 0x30
4. xor `argv[1]` with `frame_dummy`
5. compare result with encrypted flag
6. print `nice!` if flag is correct
7. mprotect to make .text section R-X
8. jump back to main

# Solving it

We can decrypt by simply XORing `enc_flag` with `frame_dummy`.

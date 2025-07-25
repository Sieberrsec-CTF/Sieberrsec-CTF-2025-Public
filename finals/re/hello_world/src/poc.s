.intel_syntax noprefix

.section .rodata
.strip_hello_world:
	.string	"Hello world!"

.section .text


strip_dumb:
	.string "\x0e\xe9\x86\xf1/l\xdc\xaa/OZ>\xf9\xbd\xff\x10y\xc6\xf9\xe4"

# first, we want to make RWX memory so we can decrypt our memory inplace
strip_make_rwx_memory:
	lea rsi, [rip]
	mov edi, 0xfff
	not rdi
	and rdi, rsi
	lea rbx, [rip+frame_dummy]
	xor rdx, rdx
	xor rsi, rsi
	xor rax, rax
	mov si, 0x1000
	mov dl, 0x7
	mov al, 0xa
	syscall
	lea r8, [rip+ENCRYPT_BEGIN]
	lea r9, [rip+ENCRYPT_END]
	xchg rsp, r14
	sub rsp, 8
	pop rax
	sub rax, strip_make_rwx_memory-strip_decrypt_memory_init
	push rax
	xchg rsp, r14
	ret

strip_dump2:
	.string "\x9f\xb6LAJVH#T\xc1\x14-\x81v\xcc\xe9\x8dPP\x8a"

# we implement our memory decryption here
strip_decrypt_memory_init:
	mov al, byte ptr [rbx]
	xor [r8], al
	inc rbx
	inc r8

	xchg rsp, r14
	sub rsp, 8
	pop rax
	cmp r8, r9 # if r8 == r9
	jnz strip_l20
	add rax, strip_check_flag_init-strip_decrypt_memory_init
strip_l20:
	push rax
	xchg rsp, r14
	ret

strip_dump3:
	.string "\x89\xfe\x8c\xc8\xa2L\xbf>\x86b\x13\xd5\xa2\xb3\x1fy\xe7w\x88\xd5"



ENCRYPT_BEGIN:

# this block of code checks argc, and calls strlen(argv[1])
strip_check_flag_init:
	cmp rbp, 0x2 # if (argc == 2) {
	jnz strip_l0 
	mov r8, [r12+8] # r8 = argv[1]
	lea r9, [rip+frame_dummy] # this is our XOR key for the enc_flag
	xor rbx, rbx # counter = 0
	# }
	# go next
strip_l0:
	xchg rsp, r14
	sub rsp, 8
	pop rax
	cmp rbp, 0x2 # if argc == 2 {
	jnz strip_l1
	sub rax, strip_check_flag_init-strip_check_flag_strlen
	# } else {
	jmp strip_l2
strip_l1:
	sub rax, strip_check_flag_init-strip_end
	# }
strip_l2:
	push rax
	xchg rsp, r14
	ret


# this block of code does `rbx = strlen(argv[1])`
# as we loop through, we will also XOR with make_rwx_memory
strip_check_flag_strlen:
	mov dl, [r8]
	test dl, dl # if (argv[1][i] == 0)
	jz strip_l3
	xor dl, [r9]
	mov [r8], dl
	inc rbx # counter += 1
	inc r8
	inc r9
	sub r14, 8
	ret
strip_l3:
	xor dl, [r9]
	mov [r8], dl
	# go next
	xchg rsp, r14
	sub rsp, 8
	pop rax
	add rax, strip_check_flag_length-strip_check_flag_strlen
	push rax
	xchg rsp, r14
	ret

.strip_enc_flag:
	.string "\x80\x6c\x6a\x9c\x37\xe0\x9b\x21\xed\x8b\x57\x3a\x2d\x7c\x79\x90\x9b\xa0\x38\x29\xeb\x98\x86\x02\x8a\x90\x8d\x39\x2c\xd6\xd4\x32\xbf\x6e\xc3\x78\x36\x35\x2b\xf1\xf4\x9b\xae\x84\x99\x95\xda\x7d"

.strip_nice:
	.string "nice!\n"

# check flag length == 48
strip_check_flag_length:
	xchg rsp, r14
	sub rsp, 8
	pop rax
	cmp rbx, 48
	jz strip_l6
	sub rax, strip_check_flag_length-strip_end # wrong
	jmp strip_l7
strip_l6:
	add rax, strip_check_flag_loop-strip_check_flag_length # correct
strip_l7:
	push rax
	xchg rsp, r14
	ret

# compare flag is correct using rep cmpsb
strip_check_flag_loop:
	cld
	mov rcx, rbx
	mov rdi, [rsi+8]
	lea rsi, [rip+.strip_enc_flag]
	xchg rsp, r14
	sub rsp, 8
	pop rax
	rep cmpsb # compare if flag is correct
	jz strip_l4
	sub rax, strip_check_flag_loop-strip_end
	jmp strip_l5
strip_l4:
	add rax, strip_print_flag-strip_check_flag_loop
strip_l5:
	push rax
	xchg rsp, r14
	ret

# simply prints argv[1] which should be the flag
strip_print_flag: # win conditional
	inc rax
	dec rdi # rdi = argc - 1 = 1
	mov rax, rdi
	lea rsi, [rip+.strip_nice]
	mov rdx, 6
	syscall # write(1, argv[1], strlen(argv[1]))
	xchg rsp, r14
	sub rsp, 8
	pop rax
	sub rax, strip_print_flag-strip_end
	push rax
	xchg rsp, r14
	ret


strip_end: # lose condition: make memory back to RX
	lea rsi, [rip]
	mov edi, 0xfff
	not rdi
	and rdi, rsi
	xor rdx, rdx
	xor rsi, rsi
	xor rax, rax
	mov si, 0x1000
	mov dl, 0x5
	mov al, 0xa
	syscall
	xor rbx, rbx
	ret

strip_dump4:
	.string "_\xc6\xe1i7\xf5p~\xbd\t"

ENCRYPT_END:

frame_dummy: # for LOLs, we can compile this as frame_dummy which is a commonly seen function
	# effectively the same as add QWORD PTR [r14], func2-frame_dummy
	endbr64
	xchg rsp, r14
	sub rsp, 8
	pop rax
	add rax, strip_make_rwx_memory-frame_dummy
	push rax
	xchg rsp, r14
	.byte 0xca
	.byte 0xfe
	.byte 0xba
	.byte 0xbe
	.byte 0x00
	# we add some null bytes here to create space for jmp register_tm_clones

// main function
.globl	main
.type	main, @function
main:
	push	rbp
	mov	rbp, rsp
	lea	rax, .strip_hello_world[rip]
	mov	rdi, rax
	call	puts@PLT
	mov	eax, 0
	pop	rbp
	ret

// constructor array
# .section	.init_array,"aw"
# .align 8
# .quad	frame_dummy
# .section	.rodata

// non executable stack
.section	.note.GNU-stack,"",@progbits

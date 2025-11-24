global _start

section .text
_start:
    ; Reserve 0x100 bytes on the stack for local buffer
    enter 0x100, 0x0

    ; Call the timer function to set an alarm
    call set_alarm

    ; Syscall: write(stdout, msg, msg_len)
    mov rax, 0x1          ; syscall number for write
    mov rdi, rax          ; file descriptor 1 (stdout)
    lea rsi, [rel msg]    ; pointer to message
    mov edx, msg_len      ; message length
    syscall

    ; Syscall: read(stdin, rsp, 0x1000)
    xor eax, eax          ; syscall number 0 (read)
    xor edi, edi          ; file descriptor 0 (stdin)
    mov rsi, rsp          ; buffer on stack
    mov edx, 0x1000       ; number of bytes to read
    syscall

    leave
    ret

set_alarm:
    ; Syscall: alarm(15)
    mov edi, 15
    mov eax, 37           ; syscall number for alarm
    syscall
    ret

section .data
    msg: db "As a pup, the wolf YEARNED for the /bin/sh"
    msg_len: equ $ - msg


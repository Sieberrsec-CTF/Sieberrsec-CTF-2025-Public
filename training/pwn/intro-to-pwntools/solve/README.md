# Introduction to Pwntools

Refer to [`solution.py`](solution.py) for the script.

This is a challenge to introduce players to scripting with pwntools.

## Solution

Connecting to challenge via netcat, we see this:

```
Welcome to the introduction to pwntools exercise!
In this exercise, your goal is to earn a total of 50 points.

We will be providing you with 2 numbers, and you should use pwntools and python to multiply the 2 numbers together.
A correct answer will garner you 1 point.
n1: 669
n2: 56
What is the value when n1 is multiplied by n2?
```

Basically, the goal of this challenge is to multiply the 2 given numbers (n1 and n2) together.

To do so, we can use pwntools.

```python

for i in range(50):
    # get n1
    io.recvuntil(b'n1: ')
    n1 = int(io.recvline())
    # get n2
    io.recvuntil(b'n2: ')
    n2 = int(io.recvline())

    # calculate n1 * n2
    print(n1,n2)
    output = n1 * n2

    # send n1 * n2 as input
    io.sendline(str(output))

io.interactive()
```


# Dungeon Monster

There is an integer overflow vulnerability.

Char has a value range of -128 to 127.

If you heal the monster 4 times, the monster's health will be greater than 127, and it will integer underflow, hence becoming negative. You will hence win.
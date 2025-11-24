# Moss in the Backrooms — Author’s Write-up

## Solution

The challenge title hints at MSB steganography, a technique where each bit of a hidden message is stored as the most significant bit (MSB) of a byte in the cover file.

In addition, if the file is opened in a hex editor (e.g. `xxd`, https://hexed.it), two things stand out:

* There are many bytes with values like `0x80` (which is `10000000` in binary).
* The JPEG header appears mostly intact, except that the first byte’s MSB is altered.

These also hint at MSB steganography.

To retrieve the hidden message:

1. Extract the MSB (bit 7) from each byte in the file.
2. Concatenate those bits into a binary string.
3. Convert the binary string into bytes to get the flag.

See `solve.py` for a solution script.

Alternatively, here's a CyberChef recipe: https://gchq.github.io/CyberChef/#recipe=Bit_shift_right(7,'Logical%20shift')Substitute('%5C%5Cx00','0',false)Substitute('%5C%5Cx01','1',false)From_Binary('None',8)

Note: When using `print()` in Python, take care not to output any extra characters after the flag, as previous output may be erased or overwritten by backspace characters.

## How MSB Works (Example):

Suppose we want to encode the character `'a'`. The ASCII value of `'a'` is 97, which in binary is:

```
97 → 0b01100001
```

This gives 8 bits: `0 1 1 0 0 0 0 1`

Now, imagine `'a'` is to be hidden in the word `"Innocent"` by manipulating the MSB of each character’s byte:

| **Position**                  | 1        | 2        | 3        | 4        | 5        | 6        | 7        | 8        |
| ----------------------------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- |
| **Original character**        | I        | n        | n        | o        | c        | e        | n        | t        |
| **Binary (original)**         | 01001001 | 01101110 | 01101110 | 01101111 | 01100011 | 01100101 | 01101110 | 01110100 |
| **Bit of `a` to encode**      | 0        | 1        | 1        | 0        | 0        | 0        | 0        | 1        |
| **New binary (with MSB set)** | 01001001 | 11101110 | 11101110 | 01101111 | 01100011 | 01100101 | 01101110 | 11110100 |
| **Resulting character**       | I        | î        | î        | o        | c        | e        | n        | ô        |

Result: `"Iîîocenô"`
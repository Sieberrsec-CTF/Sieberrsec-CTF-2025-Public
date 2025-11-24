# Feminist Literature &mdash; Author's Writeup

## Solution

`.epub` files (among others) are, in essence, ZIP archives in disguise. You may use `unzip` to extract the contents and browse through them to locate the flag.

Alternatively, `strings | grep` can be used on the `.epub`, as the contents are neither compressed nor encrypted.

## References

- Original eBook downloaded from: https://www.gutenberg.org/ebooks/3420
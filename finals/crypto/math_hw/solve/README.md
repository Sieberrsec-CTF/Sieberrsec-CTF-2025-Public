# Solution writeup here

Include e.g. images, an exploit script.

## Writeup (Math_Hw)

We know that '0', '1', '2' and '3' exist somewhere in `test_secret`, and we know it starts with `sctf{` and ends with `}`.

Try all nC4 possibilities of the positions of '0', '1', '2' and '3', then use linear algebra to solve for the rest of the secret accordingly.

# Solution writeup here

Include e.g. images, an exploit script.

## Example Writeup (SCTF 5.0: flag integer overflow)

To find the private key from the public key, notice how the generator, modulus choice is not secure

By binomial theorem, we notice that $(p + 1)^a \equiv a \cdot p + 1 \space (mod \space p^2)$

Hence, we can trivially retrieve the private key by taking $a = \frac{A - 1}{p}$

To crack the RSA, we notice that the choice of n is insecure and easily factorisable with sagemath's `factor` function. Calculating $\phi(n)$ and retrieving the original text is now trivial.

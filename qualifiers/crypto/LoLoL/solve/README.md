## Writeup (LoLoL)

We can't solve this with linear algebra methods, as setting up the matrix multiplication equation gives us a nullity of 2. In other words, we can fix any 2 values to be any value under 2 ** 80 and there would still exist a solution.

Instead, since the LHS has such small values relative to the RHS, we simply use LLL. In fact, LLL is so powerful here we only need 1 column and its output to do it.

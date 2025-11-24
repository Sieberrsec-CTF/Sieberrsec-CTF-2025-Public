# Solution writeup 

By popping the executable into your favourite decompiler, you should be greeted with a very long string of if-conditions to satisfy for `"valid flag!"` to be printed. More specifically, it is a system of 50 linear equations and 50 unknowns, but that does not really matter in the context of this solve in my opinion.

Such a challenge calls for tools which allow you to solve for a system of constraints automatically, such as Z3 and angr. Unfortunately I could not figure out how to get angr to work, so in this example I will be using Z3.

By copying the conditions from Ghidra and doing a few replaces here and there to make it fit into Z3's solver function and Python's syntax, we obtain the ASCII numbers corresponding to the characters in the flag.

See `solve.py` for solvescript.
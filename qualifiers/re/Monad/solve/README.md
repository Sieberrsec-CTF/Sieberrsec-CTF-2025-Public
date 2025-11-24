# Solution writeup here

The challenge file contains powershell code that uses a series of obfuscations to render it almost completely unreadable. Our goal would be to reverse engineer it to hopefully recover the flag.  

Deobfuscating the code reveals that the code does the following:
- Reads `flag.txt` containing the flag
- Applies a caesar cipher shift of `-7`
- Swaps every two characters in the flag
- Reverses and outputs the entire flag string

With this knowledge, we can easily write a script to reverse the transformations.  

See `solve.py` for the solve script.  
See `deobf.ps1` for the deobfuscated challenge source code.

## References

- https://github.com/t3l3machus/PowerShell-Obfuscation-Bible
- https://book.jorianwoltjer.com/reverse-engineering/powershell
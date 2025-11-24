# aes in my forens? &mdash; Author's Writeup

## Solution

When creating AES-256 encrypted, password-protected Zip archives, PBKDF2 is used to derive the encryption key. In this context, PBKDF2 is typically configured to use HMAC-SHA1 as its pseudorandom function. HMAC, in turn, specifies that if the password (used as the HMAC key) exceeds the hash function’s block size (64 bytes for SHA-1), it must first be hashed into a digest. This digest is then used in place of the original password. Consequently, the hash `9b9a2f352b707449bb52b660643df2a9a02752b4` can serve as a substitute for the original password, provided it is represented in raw byte form.

See `solve.py` for a solution script.

## References

- https://www.bleepingcomputer.com/news/security/an-encrypted-zip-file-can-have-two-correct-passwords-heres-why/
- https://en.wikipedia.org/wiki/PBKDF2

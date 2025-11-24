# sniping

The challenge provides the encryption source and an encrypted message. Encryption used is just a regular LFSR stream cipher.  
In the source code, we find that there is partial plaintext available that we can exploit.  
Using the Berlekamp Massey algorithm, we can recover the taps used in the LFSR. Since we have partial plaintext, we can recover the state of the LFSR for the first part of encryption and use the uncovered taps to continue generating the stream. This will allow us to get the flag.

Solution code can be found in `sol.py`
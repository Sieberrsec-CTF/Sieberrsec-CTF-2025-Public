# sniping

The challenge provides the encryption source and an encrypted message. Encryption used is the same as previous sniping chall but with 3 LFSRs this time.  
Notice that we are now provided with a longer partial plaintext. We make the observation that 3 LFSRs combined by XOR can be modelled with a single longer LFSR. We can use the Berlekamp Massey algorithm again with the same code to solve the challenge.

Solution code can be found in `sol.py`
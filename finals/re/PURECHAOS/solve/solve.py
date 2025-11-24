from pwn import xor
from Crypto.Util.number import long_to_bytes

flag = 646263314283424739987002908702778710263914144160199242741913731462827207958357410284387841691659606899852227119959484715233649474068629727472407689624385628

flag = long_to_bytes(flag)

# xor with known plaintext to reveal key (CP!!!)
print(xor(flag, b'sctf{')) 

# xor with key
print(xor(flag, b'CP!!!'))
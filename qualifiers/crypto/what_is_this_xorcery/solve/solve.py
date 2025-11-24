def xor(data: bytes, key: bytes) -> bytes:
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

with open("../dist/out.txt", "rb") as f:
    encrypted = f.read()

known_prefix = b"sctf{"
key_len = len(known_prefix)

recovered_key = bytes([encrypted[i] ^ known_prefix[i] for i in range(key_len)])
print(f"[+] Recovered key: {recovered_key.hex()}")

decrypted = xor(encrypted, recovered_key)
print(f"[+] Flag: {decrypted.decode()}")

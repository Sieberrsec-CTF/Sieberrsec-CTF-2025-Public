#!/usr/local/bin/python
from Crypto.Cipher import AES
import random

SZ = 16

def main():
    key = random.randbytes(16)
    iv = random.randbytes(12)
    aad = random.randbytes(8)
    tried = False
    while True:
        print("1. Encrypt GCM\n2. Encrypt ECB\n3. Decrypt ECB\n4. Reset Keys\n5. Get Flag\n")
        x = int(input(">> "))
        if x == 1:        
            pt = bytes.fromhex(input(">> "))
            cipher = AES.new(key, AES.MODE_GCM, iv)
            cipher.update(aad)
            ct, tag = cipher.encrypt_and_digest(pt)
            print("ct:", ct.hex())
            print("tag:", tag.hex())
        elif x == 2:
            pt = bytes.fromhex(input(">> "))
            cipher = AES.new(key, AES.MODE_ECB)
            ct = cipher.encrypt(pt)
            print("ct:", ct.hex())
        elif x == 3:
            ct = bytes.fromhex(input(">> "))
            cipher = AES.new(key, AES.MODE_ECB)
            pt = cipher.decrypt(ct)
            print("pt:", pt.hex())
        elif x == 4:
            key = random.randbytes(16)
            iv = random.randbytes(12)
            aad = random.randbytes(8)
            print("Reset.")
        elif x == 5:
            if tried:
                print("nah.")
                continue
            challenge = random.randbytes(32)
            print("Challenge:", challenge.hex())
            ct = bytes.fromhex(input(">> "))
            tag = bytes.fromhex(input(">> "))
            cipher = AES.new(key, AES.MODE_GCM, iv)
            cipher.update(aad)
            if cipher.decrypt_and_verify(ct, tag) == challenge:
                print(open("/app/flag.txt","rb").read())
            tried = True

if __name__ == "__main__":
    main()
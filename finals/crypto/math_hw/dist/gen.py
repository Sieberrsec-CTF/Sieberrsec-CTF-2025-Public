#!/usr/local/bin/python
from random import randrange, choices
from hashlib import sha256
import string
import time

n = 131 # we will perform matrix multiplications under modulo n

sanity_check = ['0', '1', '2', '3']

def main():
    for attempt in range(3):
        while True:
            test_secret = 'sctf{' + ''.join(choices(string.printable[:-5], k=15)) + '}'
            
            # check that our secret fulfils sanity check
            passed = True
            for char in sanity_check:
                passed &= char in test_secret
            
            if passed:
                break

        k = len(test_secret)

        # defining a 1 x k row vector A. unfortunately i forgot to print it out :(
        A = [ord(ch) for ch in test_secret]

        # my homework worksheet matrix is this k x (k - 10) with random values
        B = [[randrange(n) for _ in range(k - 10)] for __ in range(k)]

        # doing my homework! calculating C = A * B, a 1 x (k - 10) row vector
        C = [sum([A[idx] * B[idx][idx2] for idx in range(k)]) % n for idx2 in range(k - 10)]

        secret_hash = sha256(test_secret.encode('utf-8')).hexdigest()

        print("B = [")
        for row in B:
            print(f"\t{row}" + ("," if row != B[-1] else ""))
        print("]")
        print(f"{C = }")
        print(f"{secret_hash = }")

        start_time = time.time()

        cand_ans = input("Find the secret and report it back to me: ")

        end_time = time.time()
        elapsed_time = end_time - start_time

        if cand_ans == test_secret:
            if elapsed_time < 30:
                if attempt == 2:
                    with open('flag.txt', 'r') as handler:
                        flag = handler.read()
                    print(f"You got it! Here is your flag:\n{flag}")
                else:
                    print(f"You got it! {2 - attempt} more times to go :D")
            else:
                print("Too slow! Try again :(")
                return
        else:
            print("Wrong answer! Try again :(")
            return

if __name__ == '__main__':
    main()

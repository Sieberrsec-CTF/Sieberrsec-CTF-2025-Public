#!/usr/bin/python3.9 -u

from base64 import b64decode
import os
from uuid import uuid4

inp = input("base64 encoded script > ")

recv = b64decode(inp)

filename = str(uuid4())
with open(f"/tmp/{filename}", "wb") as file:
    file.write(recv)

os.system(f"/usr/bin/python3.9 /app/run.py {filename}")
os.system(f"/usr/bin/rm /tmp/{filename}")

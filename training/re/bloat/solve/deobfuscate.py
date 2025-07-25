import re
with open("bloat.py", "r") as handler:
    obfuscated_code = handler.read()

a = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ"+ \
            "[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~ "

clean_code = obfuscated_code

# replace all a[0], a[1], ... a[-1] with the actual string
for idx in range(len(a)):
    clean_code = clean_code.replace(f"a[{idx}]", f"\'{a[idx]}\'")

# merge all adjacent strings
clean_code = clean_code.replace("\'+\'", "")
clean_code = clean_code.replace("\'+\\\n\'", "")

with open("clean.py", "w") as handler:
    handler.write(clean_code)
from Crypto.Util.number import long_to_bytes, bytes_to_long, getPrime
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
import hashlib
from random import randrange
# run `pip install pycryptodome` if it is not currently installed


def encrypt(pt : str, shared_key : int) -> int:
    pt_bytes = pt.encode()
    hash = hashlib.sha256(str(shared_key).encode()).digest()
    key, iv = hash[16:], hash[:16]

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    ct = cipher.encrypt(pad(pt_bytes, AES.block_size))
    return bytes_to_long(ct)

def decrypt(ct: int, shared_key : int):
    ct_bytes = long_to_bytes(ct)
    hash = hashlib.sha256(str(shared_key).encode()).digest()
    key, iv = hash[16:], hash[:16]

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)

    pt_padded = cipher.decrypt(ct_bytes)
    pt_bytes = unpad(pt_padded, AES.block_size)
    return pt_bytes.decode()

flag = "sctf{redacted}"

# N is our modulus
N = getPrime(1024)

# g is our generator
g = 2

# a and A are Alice's private and public keys respectively
a = randrange(1024, N)
A = pow(g, a, N)

# b and B are Bob's private and public keys respectively
b = randrange(1024, N)
B = pow(g, b, N)

# Bob gets the shared key with Alice's public key and his private key
shared_key = pow(A, b, N)
ct = encrypt(flag, shared_key)

print(f"{N = }")
print(f"{a = }")
print(f"{A = }")
print(f"{B = }")
print(f"{ct = }")

# After you find shared_key, use the decrypt function to recover the original flag
pt = decrypt(ct, shared_key)
print(f"{pt = }")

# Output:
# N = 178662735391826349032294453760089651952324412338358712816289351842082073405579016221886700936757320378430049923755584857143010742513042922923387153329142432197932450583181225964592919323945205551524260900813013698827045341083918336910183408284405161420613254774565381238063339619972061907249803930793796683209
# a = 156762527849594309200517664370198867652131441910799320006953595611009187607301700389014840137750142382526321161418892998876301130142106875298403227270177089052179390090375655093327505944118375898373569167695828376129591125723235247135391027945476618702476431539806704168472988466037537171936603561782452892119
# A = 175978614629768252857388888813825784906351702252488736934183242710590392433263855182886398841294667122037414982352115797467249800752110279814277240132652637599486387172666661298977548359340902581290474845357855947913546296103958177235402553954773242675428297020131985273629809682589163814773603614360024846368
# B = 104094387318002456223309112058645599581034066795926501392466672433717054625569280988275407153039617338137940474012185760988202641489087293669133975607884059517975011172747873247920758428898662964333977650228307343186623842404378208626730242345536766517259365176195138873575760841479077874862341871446183615097
# ct = 7189854005713452450392883616838564556171333962722439154094120482472182116830
# pt = 'sctf{REDACTED}'
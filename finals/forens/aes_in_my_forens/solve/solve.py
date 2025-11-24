import pyzipper

sha1 = bytes.fromhex("9b9a2f352b707449bb52b660643df2a9a02752b4")

with pyzipper.AESZipFile('aes_in_my_forens.zip') as zf:
    zf.setpassword(sha1)
    data = zf.read('falg.txt')
    print(data.decode('utf-8'))
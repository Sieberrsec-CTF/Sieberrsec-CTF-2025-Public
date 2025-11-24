def xor_bytes(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

ct = bytes.fromhex("d5fea4dc0c8f48e2d8542f1a3fc5ed19f2ba519edb34f63c02a1b0792dacbc85ac2eb994b475c3e82eb27ae365ecf6324bf0d93f20ed88781aae0234fbfed34e1f081607a8b1710b866bf1296d65243c0f5288618ab6ace0a9c3c904e8651caffc2331bbefb7619fd9e8e0d194e7ba08a7")
known_pt = bytes.fromhex(b"balls the flag is gullible balls balls balls balls balls balls balls balls balls balls balls balls balls balls balls".hex())
known_ct = bytes.fromhex("c4fcbcd604c849e6d11d2b1a3bfdaa05edf60789db3dc0391ba8fc2a2eace3a9eb39e9c9b1648fef10b963a174bff53242dc9e2870b0d56956ff3c6ee2e19f451c081f2bbea6210b837abd2e533f3d7e43018b61d59acbd784e3ec3584422284c5612090cc973eb39effedd191f6f60fbb3c7c0d")

stream = xor_bytes(known_pt, known_ct)
flag = xor_bytes(ct, stream)
print(flag.decode())
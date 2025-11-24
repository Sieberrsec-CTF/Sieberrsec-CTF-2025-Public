import numpy
import copy

# taken from https://gist.github.com/StuartGordonReid/a514ed478d42eca49568
def berlekamp_massey_algorithm(block_data):
    """
    An implementation of the Berlekamp Massey Algorithm. Taken from Wikipedia [1]
    [1] - https://en.wikipedia.org/wiki/Berlekamp-Massey_algorithm
    The Berlekamp-Massey algorithm is an algorithm that will find the shortest linear feedback shift register (LFSR)
    for a given binary output sequence. The algorithm will also find the minimal polynomial of a linearly recurrent
    sequence in an arbitrary field. The field requirement means that the Berlekamp-Massey algorithm requires all
    non-zero elements to have a multiplicative inverse.
    :param block_data:
    :return:
    """
    n = len(block_data)
    c = numpy.zeros(n)
    b = numpy.zeros(n)
    c[0], b[0] = 1, 1
    l, m, i = 0, -1, 0
    int_data = [int(el) for el in block_data]
    while i < n:
        v = int_data[(i - l):i]
        v = v[::-1]
        cc = c[1:l + 1]
        d = (int_data[i] + numpy.dot(v, cc)) % 2
        if d == 1:
            temp = copy.copy(c)
            p = numpy.zeros(n)
            for j in range(0, l):
                if b[j] == 1:
                    p[j + i - m] = 1
            c = (c + p) % 2
            if l <= 0.5 * i:
                l = i + 1 - l
                m = i
                b = temp
        i += 1
    return l, c

from Crypto.Util.number import long_to_bytes

class LFSR:
      def __init__(self, seed, taps, length):
          self.state = seed
          self.taps = taps
          self.length = length
          
      def getBit(self):
          return self.state & 1
          
      def __next__(self):
          xor = self.state & self.taps
          out = bin(xor).count('1') % 2
          self.state = ((self.state << 1) + out) % (2**self.length)
          return out
      
      def __iter__(self):
          return self

def xor(a, b):
    return bytes(i ^ j for i, j in zip(a, b))

_enc = 0x4b8bd9aa0d4477573760bc0a2c38b12f72b1891341236680eb6277d6a177724c3f479893aa4a521516c64fabe10c4c626985cd8c8799494e761ed8679005173cdf1d1e7fc1cc4c88c0b15395acb991df6a317ed94c9296044a536a5e8
enc = long_to_bytes(_enc)
ppt = b'This time,  the flag is: sctf{'
seq = xor(ppt, enc[:len(ppt)])
seq = bin(int.from_bytes(seq))[2:].zfill(8*len(ppt))

poly = berlekamp_massey_algorithm(seq)
l = poly[0]
c = poly[1][1:l+1][::-1].astype(int)
c = ''.join(map(str, c))
print(l)
print(c)

lfsr = LFSR(int(seq[:l], 2), int(c, 2), l)
stream = seq[:l] + ''.join([str(next(lfsr)) for _ in range(((_enc.bit_length() + 7) // 8) * 8 - l)])
flag = xor(enc, long_to_bytes(int(stream, 2)))
print(flag)
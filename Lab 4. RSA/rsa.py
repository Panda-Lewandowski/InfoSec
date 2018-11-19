import sys
from base64 import *
from Crypto.Util import number
from random import randrange


class baseconv(object):
    def __init__(self):
        self.chars = '0123456789'
        self.base = len(self.chars)
        self.splitter = "!"
        self.debug = False

    @staticmethod
    def basealpha_encode(chars, base, binary):
        encoded = ''
        while int(binary) > 0:
            binary, remainder = divmod(binary, base)
            encoded = chars[remainder] + encoded
        return encoded

    @staticmethod
    def basealpha_decode(chars, base, charset):
        i = 1
        res = 0
        for char in charset:
            res += chars.index(char) * i
            i *= base
        return chr(res)

    def tobase(self, string):
        res = ''
        for char in string:
            res += self.basealpha_encode(self.chars, self.base, ord(char)) + self.splitter
        return res

    def frombase(self, enc):
        res = ''
        charlist = enc.split(self.splitter)
        charlist.pop()
        for word in charlist:
            res += self.basealpha_decode(self.chars, self.base, word[::-1])
        return res


class RSA(object):
    def __init__(self, p=None, q=None, bits=8):
        if not p:
            p = number.getPrime(bits)
        if not q:
            q = number.getPrime(bits)
        self.p = p if number.isPrime(p) else exit(-1)
        self.q = q if number.isPrime(q) else exit(-1)
        self.n = p * q
        self.phi = (p - 1) * (q - 1)
        self.e = self.get_e(self.phi, bits)
        self.d = self.get_d(self.e, self.phi)

    def crypt(self, char, key):
        #if char == splitter:
        #    return splitter
        '''
        С = M**e mod N
        M’ = C**d mod N
        '''
        return char**key % self.n

    def encrypt_string(self, string):
        res = ""
        for char in string:
            ch = self.crypt(ord(char), self.d)
            #print("Char->char: ", char, ch)
            res += chr(ch)
            #print(char, type(char))
        return res

    def decrypt_string(self, string):
        res = ""
        for char in string:
            ch = self.crypt(ord(char), self.e)
            #print("char->dchar: ", ord(char), ch)
            res += chr(ch)
        return res

    @staticmethod
    def get_d(e, phi):
        return number.inverse(e, phi)

    @staticmethod
    def get_e(phi, bits=192):
        # (e*d) mod fi == 1
        while True:
            result = randrange(2,255)
            modulus = number.GCD(result, phi)
            if modulus == 1:
                return result

    @staticmethod
    def get_greatest_common_divisor(a, b):
        while b != 0:
            a, b = b, a % b
        return a


if __name__ == '__main__':
    if len(sys.argv) < 2:
        str = "Test string"
        print("Source : ", str)
        #basis = baseconv()
        rsa = RSA(p=199,q=179)
        print("\tP:", rsa.p, "\n\tQ:", rsa.q, "\n\tE:", rsa.e, "\n\tN:", rsa.n, "\n\tD:", rsa.d)
        enc = b64encode(str.encode("ascii"))
        print("Encoded: ", enc, "Length: ", len(enc))
        rsaed = rsa.encrypt_string(enc.decode("ascii"))
        print("rsa-ed: ", rsaed)
        dersaed = rsa.decrypt_string(rsaed)
        print("De-rsa: ", dersaed)
        dec = b64decode(dersaed)
        print("Decoded: ", dec)
        print("Deciphered: ", dec.decode("ascii"))
    else:
        filename = sys.argv[1]
        with open(filename, 'rb') as file1:
            data = file1.read()
            #basis = baseconv()
            rsa = RSA(p=199,q=179)
            print("\tP:", rsa.p, "\n\tQ:", rsa.q, "\n\tE:", rsa.e, "\n\tN:", rsa.n, "\n\tD:", rsa.d)
            str = b32encode(data)
            #b26 = basis.tobase(str.decode("utf-8"))
            dta = str.decode("ascii")
            print("Encrypting...")
            enc = rsa.encrypt_string(dta)
            with open(filename + ".encrypted", 'w') as file2:
                file2.write(enc)
                file2.close()
            print("Decrypting...")
            dec = rsa.decrypt_string(enc)
            with open(filename + ".decrypted", 'w') as file3:
                file3.write(dec)
                file3.close()
            #bkup = basis.frombase(dec)
            restored = b32decode(dec)
            with open(filename + ".restored", 'wb') as file4:
                file4.write(restored)
                file4.close()

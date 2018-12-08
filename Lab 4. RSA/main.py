from base64 import b32encode, b32decode
from rsa import RSA
import sys

if __name__ == '__main__':
        filename = sys.argv[1]

        if len(sys.argv) == 2:
            rsa = RSA(p=199,q=179)
        else:
            rsa = RSA(p=int(sys.argv[3]),q=int(sys.argv[3]))
 
        with open(filename, 'rb') as file1:
            data = file1.read()
            rsa = RSA(p=199,q=179)
            print("\tP:", rsa.p, "\n\tQ:", rsa.q, "\n\tE:", rsa.e, "\n\tN:", rsa.n, "\n\tD:", rsa.d)
            str = b32encode(data)
            dta = str.decode("ascii")
            print("Encrypting...")
            enc = rsa.encrypt_string(dta)
            with open(filename.split('.')[0] + ".encrypted", 'w') as file2:
                file2.write(enc)
            print("Decrypting...")
            dec = rsa.decrypt_string(enc)
            restored = b32decode(dec)
            with open(filename.split('.')[0]  + ".decrypted", 'wb') as file4:
                file4.write(restored)
from OpenSSL import crypto
import sys


if __name__ == '__main__':
    with open(sys.argv[1], 'rb') as f:
        data = f.read()

    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 1024)
    print(f'Private and public keys were generated')
    
    cert = crypto.X509()
    cert.set_pubkey(key)

    signature = crypto.sign(key, data, "sha256")
    print(f'Created signature: {signature}')

    # OK 
    try:
        crypto.verify(cert, signature, data, "sha256")
        print('Signature checking passed ok!')
    except Exception:
        print('Wrong signature!')

    # Wrong 
    try:
        crypto.verify(crypto.X509(), signature, data, "sha256")
        print('Signature checking passed ok!')
    except Exception:
        print('Wrong signature!')

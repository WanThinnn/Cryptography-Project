import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCMSIV



def set_up():
    key = AESGCMSIV.generate_key(bit_length=256)
    nonce = os.urandom(12)
    aad = os.urandom(16)
    return key, nonce, aad


def encrypt(plaintext, key256, nonce, aad):
    aesgcmsiv = AESGCMSIV(key256)
    ciphertext = aesgcmsiv.encrypt(nonce, plaintext.encode(), aad)  # Encode plaintext to bytes
    return ciphertext


def decrypt(ciphertext, key256, nonce, aad):
    aesgcmsiv = AESGCMSIV(key256)
    decrypted_data = aesgcmsiv.decrypt(nonce, ciphertext, aad)
    return decrypted_data.decode('utf-8')


def main():
    key, nonce, aad = set_up()
    ct = encrypt("hello", key, nonce, aad)
    pt = decrypt(ct, key, nonce, aad)
    print(key)
    print(nonce)
    print(aad)
    print(ct)
    print(pt)



if __name__ == "__main__":
    main()

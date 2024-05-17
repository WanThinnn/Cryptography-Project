import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64


def ByteToBase64(key):
    return base64.b64encode(key).decode('utf-8')

def Base64ToByte(key_base64):
    return base64.b64decode(key_base64)


def gen_key_IV():
    associated_data = "Đây là dữ liệu liên quan.".encode('utf-8')
    IV = ByteToBase64(os.urandom(12))  # Tạo nonce ngẫu nhiên 16 bytes
    Key = ByteToBase64(os.urandom(32))  # AES-256
    return IV, Key, associated_data


# Hàm mã hóa sử dụng AES GCM
def encrypt_with_python(plaintext, key, IV, associated_data):
    key = Base64ToByte(key)
    IV = Base64ToByte(IV)
    aesgcm = AESGCM(key)
    plaintext_bytes = plaintext.encode('utf-8')
    ciphertext_with_tag = aesgcm.encrypt(IV, plaintext_bytes, associated_data)
    ciphertext = ByteToBase64(ciphertext_with_tag)
    return ciphertext

# Hàm giải mã sử dụng AES GCM
def decrypt_with_python(ciphertext, key, IV, associated_data):
    ciphertext = Base64ToByte(ciphertext)
    IV = Base64ToByte(IV)
    key = Base64ToByte(key)
    aesgcm = AESGCM(key)
    plaintext_bytes = aesgcm.decrypt(IV, ciphertext, associated_data)
    ciphertext = plaintext_bytes.decode('utf-8')
    return ciphertext

# Ví dụ sử dụng
IV, Key, associated_data = gen_key_IV()

plaintext = "Đây là một thông điệp bí mật."

ciphertext = encrypt_with_python(plaintext, Key, IV, associated_data)
decrypted_text = decrypt_with_python(ciphertext, Key, IV, associated_data)

print(f"Key (base64): {Key}")
print(f"IV: (Bas464): {IV}")
print(f"Encrypted message: {ciphertext}")
print(f"Decrypted text: {decrypted_text}")

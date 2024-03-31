# -*- coding: utf-8 -*-
import sys
sys.path.append("D:\\Dropbox\\UIT_WORKS\\2023_2024_Classes\\HK1\\NT219.Cryptography\\AES")
from mypackages import key_expansion
# Convert text <--> bin
def message_to_bin(message):
    """Convert a string message to its binary representation using UTF-8 encoding."""
    binary_message = ''.join(format(byte, '08b') for byte in message.encode('utf-8'))
    return binary_message

##Main
#Test key 128
key128="12345678abcdefgh"
key_bytes_128 = key128.encode('utf-8')
AES128_keys = key_expansion.key_expansion(key_bytes_128).key_expansion_128()
print(AES128_keys,len(AES128_keys))

#Test key 192
key192="12345678abcdefghvbnmfgds"
key_bytes_192 = key192.encode('utf-8')
AES192_keys = key_expansion.key_expansion(key_bytes_192).key_expansion_192()
print(AES192_keys,"number of words:",len(AES192_keys))

#Test key 256

key256="12345678abcdefghvbnmfgds12345678"
key_bytes_256=key256.encode('utf-8')
AES256_keys = key_expansion.key_expansion(key_bytes_256).key_expansion_256()
print(AES256_keys,"number of words:",len(AES256_keys))
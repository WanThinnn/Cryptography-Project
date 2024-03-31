# Ref: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38a.pdf
import os
from .AES import AES
class modes:
    def __init__(self, key):
        key_length = len(key) * 8  # Convert key length to bits
        if key_length not in [128, 192, 256]:
            raise ValueError("Invalid key length. Supported lengths are 128, 192, and 256 bits.")
        self.aes = AES(key, key_length)  # Assuming you have an AES class that takes a key and key_length
        self.iv = os.urandom(16)
    ### Process the input data
    def utf8_to_bytes(self, utf8_str):
        """Convert a UTF-8 string to bytes."""
        return utf8_str.encode('utf-8')
    def bytes_to_utf8(self, bytes_data):
        """Convert bytes to a UTF-8 string."""
        return bytes_data.decode('utf-8')
    
    ### Binary string <--> bytes with padding if necessary
    def binary_to_bytes(self, binary_str):
        """Convert a binary string to bytes with padding if necessary."""
        # Calculate the number of padding bits needed
        padding_length = 8 - (len(binary_str) % 8)
        # Apply padding: append a '1' followed by necessary '0's
        binary_str += '1' + '0' * (padding_length - 1)
        n = int(binary_str, 2)
        byte_length = len(binary_str) // 8
        return n.to_bytes(byte_length, 'big')

    def bytes_to_binary(self, bytes_data):
        """Convert bytes to a binary string and remove padding."""
        binary_str = bin(int.from_bytes(bytes_data, 'big'))[2:]
        # Find the last '1' (indicating the start of padding) and remove it along with all following '0's
        last_one_index = binary_str.rfind('1')
        return '0b' + binary_str[:last_one_index]
    
    #############Padding bytes     
    def pkcs7_padding(self, data):
        """Apply PKCS7 padding."""
        # If data is a UTF-8 string, encode it to bytes
        if isinstance(data, str):
            data = data.encode('utf-8')
        # If data is a binary string, convert it to bytes
        elif data.startswith('0b'):
            data = self.binary_to_bytes(data[2:])
        
        padding_length = 16 - (len(data) % 16)
        return data + bytes([padding_length] * padding_length)

    def pkcs7_unpadding(self, data):
        """Remove PKCS7 padding."""
        padding_length = data[-1]
        return data[:-padding_length]
   ## ECB mode 
    def ecb_encrypt(self, plaintext):
        # Apply padding
        padded_data = self.pkcs7_padding(plaintext)

        # Encrypt each block
        encrypted_blocks = []
        for i in range(0, len(padded_data), 16):
            block = padded_data[i:i+16]
            encrypted_block = self.aes.encrypt(block)
            encrypted_blocks.append(encrypted_block)
        return b''.join(encrypted_blocks)

    def ecb_decrypt(self, ciphertext):
        if len(ciphertext) % 16 != 0:
            raise ValueError("Ciphertext length must be a multiple of 16 bytes for ECB mode.")

        decrypted_blocks = []
        for i in range(0, len(ciphertext), 16):
            block = ciphertext[i:i+16]
            decrypted_block = self.aes.decrypt(block)
            decrypted_blocks.append(decrypted_block)
        # Remove padding
        decrypted_data = self.pkcs7_unpadding(b''.join(decrypted_blocks))
        return decrypted_data.decode('utf-8')

#CBC mode
    def cbc_encrypt(self, plaintext):
        # Apply padding
        padded_data = self.pkcs7_padding(plaintext)

        # Encrypt each block
        encrypted_blocks = []
        previous_block = self.iv
        # print("The Inital Vector IV: ", previous_block.hex())
        for i in range(0, len(padded_data), 16):
            block = padded_data[i:i+16]
            # XOR with the previous ciphertext block (or IV for the first block)
            block = bytes([block[j] ^ previous_block[j] for j in range(16)])
            encrypted_block = self.aes.encrypt(block)
            encrypted_blocks.append(encrypted_block)
            previous_block = encrypted_block

        # The IV is prepended to the ciphertext for use in decryption
        return self.iv + b''.join(encrypted_blocks)

    def cbc_decrypt(self, ciphertext):
        if len(ciphertext) % 16 != 0:
            raise ValueError("Ciphertext length must be a multiple of 16 bytes for CBC mode.")

        # Extract the IV from the ciphertext
        iv = ciphertext[:16]
        # print("The Inital Vector IV: ", iv.hex())
        ciphertext = ciphertext[16:]

        decrypted_blocks = []
        previous_block = iv
        # print("The Inital Vector IV: ", previous_block.hex())
        for i in range(0, len(ciphertext), 16):
            block = ciphertext[i:i+16]
            decrypted_block = self.aes.decrypt(block)
            # XOR with the previous ciphertext block (or IV for the first block)
            decrypted_block = bytes([decrypted_block[j] ^ previous_block[j] for j in range(16)])
            decrypted_blocks.append(decrypted_block)
            previous_block = block

        # Remove padding
        decrypted_data = self.pkcs7_unpadding(b''.join(decrypted_blocks))
        return decrypted_data.decode('utf-8')
    ## CFB-64, CFB-128

    def cfb_encrypt(self, plaintext, segment_size=128):
        if segment_size not in [64, 128]:
            raise ValueError("Segment size must be either 64 or 128 for CFB mode.")

        segment_bytes = segment_size // 8

        # Ensure plaintext is in bytes format
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        encrypted_blocks = []
        previous_block = self.iv
        print("The Inital Vector IV: ", previous_block.hex())
        for i in range(0, len(plaintext), segment_bytes):
            segment = plaintext[i:i+segment_bytes]
            encrypted_iv = self.aes.encrypt(previous_block)
            encrypted_segment = bytes([segment[j] ^ encrypted_iv[j] for j in range(len(segment))])
            encrypted_blocks.append(encrypted_segment)
            if segment_size == 64:
                previous_block = previous_block[segment_bytes:] + encrypted_segment
            else:
                previous_block = encrypted_segment

        # The IV is prepended to the ciphertext for use in decryption
        return self.iv + b''.join(encrypted_blocks)


    def cfb_decrypt(self, ciphertext, segment_size=128):
        if segment_size not in [64, 128]:
            raise ValueError("Segment size must be either 64 or 128 for CFB mode.")

        segment_bytes = segment_size // 8

        # Extract the IV from the ciphertext
        iv = ciphertext[:16]
        ciphertext = ciphertext[16:]

        decrypted_blocks = []
        previous_block = iv
        print("The Inital Vector IV: ", previous_block.hex())
        for i in range(0, len(ciphertext), segment_bytes):
            segment = ciphertext[i:i+segment_bytes]
            encrypted_iv = self.aes.encrypt(previous_block)
            decrypted_segment = bytes([segment[j] ^ int(encrypted_iv[j]) for j in range(len(segment))])
            decrypted_blocks.append(decrypted_segment)
            if segment_size == 64:
                previous_block = previous_block[segment_bytes:] + segment
            else:
                previous_block = segment

        return b''.join(decrypted_blocks).decode('utf8')
    # OFB Implementation
    def ofb_encrypt(self, plaintext):
        """
        Encrypts the given plaintext using the OFB mode.
        """
        # Apply padding
        padded_data = self.pkcs7_padding(plaintext)

        encrypted_blocks = []
        previous_block = self.iv
        print("The Inital Vector IV: ", previous_block.hex())
        for i in range(0, len(padded_data), 16):
            block = padded_data[i:i+16]
            encrypted_iv = self.aes.encrypt(previous_block)
            encrypted_block = bytes([block[j] ^ encrypted_iv[j] for j in range(len(block))])
            encrypted_blocks.append(encrypted_block)
            previous_block = encrypted_iv

        return self.iv + b''.join(encrypted_blocks)

    def ofb_decrypt(self, ciphertext):
        """
        Decrypts the given ciphertext using the OFB mode.
        """
        self.iv = ciphertext[:16]
        ciphertext = ciphertext[16:]
        decrypted_blocks = []
        previous_block = self.iv
        print("The Inital Vector IV: ", previous_block.hex())
        for i in range(0, len(ciphertext), 16):
            block = ciphertext[i:i+16]
            encrypted_iv = self.aes.encrypt(previous_block)
            decrypted_block = bytes([block[j] ^ encrypted_iv[j] for j in range(len(block))])
            decrypted_blocks.append(decrypted_block)
            previous_block = encrypted_iv

        # Remove padding
        decrypted_data = self.pkcs7_unpadding(b''.join(decrypted_blocks))
        return decrypted_data.decode('utf-8')
    def ctr_encrypt(self, plaintext):
        """
        Encrypts the given plaintext using the CTR mode.
        """
        # No padding is required for CTR mode
        encrypted_blocks = []
        print("The Inital Vector IV: ", self.iv.hex())
        counter = int.from_bytes(self.iv, byteorder='big')  # Convert IV to a big-endian integer
        # Ensure plaintext is in bytes format
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        for i in range(0, len(plaintext), 16):
            block = plaintext[i:i+16]
            encrypted_counter = self.aes.encrypt(counter.to_bytes(16, byteorder='big'))
            encrypted_block = bytes([block[j] ^ encrypted_counter[j] for j in range(len(block))])
            encrypted_blocks.append(encrypted_block)
            counter += 1

        return self.iv + b''.join(encrypted_blocks)

    def ctr_decrypt(self, ciphertext):
        """
        Decrypts the given ciphertext using the CTR mode.
        """
        iv = ciphertext[:16]
        print("The Inital Vector IV: ", iv.hex())
        ciphertext = ciphertext[16:]
        decrypted_blocks = []
        counter = int.from_bytes(iv, byteorder='big')  # Convert IV to a big-endian integer

        for i in range(0, len(ciphertext), 16):
            block = ciphertext[i:i+16]
            encrypted_counter = self.aes.encrypt(counter.to_bytes(16, byteorder='big'))
            decrypted_block = bytes([block[j] ^ encrypted_counter[j] for j in range(len(block))])
            decrypted_blocks.append(decrypted_block)
            counter += 1

        return b''.join(decrypted_blocks).decode('utf-8')

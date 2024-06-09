# Import Charm-Crypto
from charm.toolbox.pairinggroup import PairingGroup, GT
from charm.schemes.abenc.ac17 import AC17CPABE
from Crypto.Cipher import AES
import hashlib
import base64
from DATA_USER_ABE.SerializeCTXT import SerializeCTXT

class CPABE:
    def __init__(self, scheme):
        if scheme == "AC17":
            self.groupObj = PairingGroup("SS512")
            self.ac17 = AC17CPABE(self.groupObj, 2)
            self.serialized = SerializeCTXT()
    
    def AC17encrypt(self, public_key, message, policy):
        random_key = self.groupObj.random(GT)
        
        # Encrypt random_key using CP-ABE
        encrypted_key = self.ac17.encrypt(public_key, random_key, policy)
        # Serialize to save to database
        encrypted_key_b = self.serialized.jsonify_ctxt(encrypted_key)
        # Create key for AES by random_key
        hash = hashlib.sha256(str(random_key).encode())
        key = hash.digest()
        aes = AES.new(key, AES.MODE_GCM)

        if type(message) != bytes:
            if type(message) != str:
                message = str(message)
    
        ciphertext, authTag = aes.encrypt_and_digest(message.encode())
        nonce = aes.nonce

        # Final ciphertext that will be sent to database
        ciphertext = nonce + ciphertext + authTag
        
        len_encrypted_data = len(encrypted_key_b)
        encrypted_data = len_encrypted_data.to_bytes(8, byteorder='big') + encrypted_key_b.encode() + ciphertext
        # Encode Base64 for encrypted_key and ciphertext

        encrypted_data = base64.b64encode(encrypted_data).decode()
        return encrypted_data
    
    def AC17decrypt(self, public_key, encrypted_data, private_key):
        encrypted_data = base64.b64decode(encrypted_data.encode())
        len_encrypted_key = int.from_bytes(encrypted_data[:8], byteorder='big')
        encrypted_key_b = encrypted_data[8:8 + len_encrypted_key]
        ciphertext = encrypted_data[8 + len_encrypted_key:]

        encrypted_key = self.serialized.unjsonify_ctxt(encrypted_key_b.decode('utf-8'))
        recovered_random_key = self.ac17.decrypt(public_key, encrypted_key, private_key)
    
        if recovered_random_key:
            nonce = ciphertext[:16]
            authTag = ciphertext[-16:]
            ciphertext = ciphertext[16:-16]

            hash = hashlib.sha256(str(recovered_random_key).encode())
            key = hash.digest()
            try:
                aes = AES.new(key, AES.MODE_GCM, nonce)
                recovered_message = aes.decrypt_and_verify(ciphertext, authTag)
                return recovered_message.decode()
            except ValueError as e:
                return None
        else:
            return None

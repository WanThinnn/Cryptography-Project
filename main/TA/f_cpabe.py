import argparse
from CPABE import CPABE
from charm.toolbox.pairinggroup import PairingGroup
from charm.core.engine.util import objectToBytes, bytesToObject
import sys
import csv
import shutil

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    input_data = {}
    for line in lines:
        key, value = line.strip().split(': ', 1)
        input_data[key] = value
    
    return input_data

def save_to_file(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)

def load_from_file(filename):
    with open(filename, 'rb') as file:
        return file.read()

def setup(cpabe, path):
    public_key, master_key = cpabe.ac17.setup()
    
    serialized_public_key = objectToBytes(public_key, cpabe.groupObj)
    serialized_master_key = objectToBytes(master_key, cpabe.groupObj)
    
    save_to_file(serialized_public_key, path+'public_key.bin')
    save_to_file(serialized_master_key, path+'master_key.bin')
    
    print(f"Keys generated and saved to {path}public_key.bin and {path}master_key.bin")


def gen_secret_key(cpabe, public_key_file, master_key_file, attributes, private_key_file):
    public_key = bytesToObject(load_from_file(public_key_file), cpabe.groupObj)
    master_key = bytesToObject(load_from_file(master_key_file), cpabe.groupObj)
    
    user_attributes = attributes.split(',')
    private_key = cpabe.ac17.keygen(public_key, master_key, user_attributes)
    
    serialized_private_key = objectToBytes(private_key, cpabe.groupObj)
    save_to_file(serialized_private_key, private_key_file)
    
    print(f"Secret Key generated and saved to {private_key_file}")

    
def encrypt_message(cpabe, public_key_file, plaintext_file, ciphertext):
    public_key = bytesToObject(load_from_file(public_key_file), cpabe.groupObj)
    
    with open(plaintext_file, 'r', newline='') as infile, open(ciphertext, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=['columns', 'key'])
        
        writer.writeheader()
        for row in reader:
            if 'key' in row and 'policy' in row and row['key']:
                row['key'] = cpabe.AC17encrypt(public_key, row['key'], row['policy'])
                writer.writerow({'columns': row['columns'], 'key': row['key']})
    
    print(f"Encrypted data saved to {ciphertext}")



def decrypt_message(cpabe, public_key_file, private_key_file, cipher_text_file, recover_text_file):
    private_key = bytesToObject(load_from_file(private_key_file), cpabe.groupObj)
    public_key = bytesToObject(load_from_file(public_key_file), cpabe.groupObj)

    with open(cipher_text_file, 'r') as infile, open(recover_text_file, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=['columns', 'key'])
        
        writer.writeheader()
        for row in reader:
            if 'key' in row and row['key']:
                decrypted_key = cpabe.AC17decrypt(public_key, row['key'], private_key)
                if decrypted_key:
                    writer.writerow({'columns': row['columns'], 'key': decrypted_key})
    
    print(f"Decrypted data saved to {recover_text_file}")

def main():
    cpabe = CPABE("AC17")
    if len(sys.argv) < 2:
        print("Usage: python3 main.py [setup|genkey|encrypt|decrypt]")
        sys.exit(1)
    
    mode =  sys.argv[1]

    if mode == 'setup':
        if len(sys.argv) < 3:
            print("Usage: python3 main.py setup <path_to_save_file>")
            sys.exit(1)
        path = sys.argv[2]
        setup(cpabe, path)
        
    if mode == 'genkey':
        if len(sys.argv) < 6:
            print("Usage: python3 main.py genkey <public_key_file> <master_key_file> <attributes> <private_key_file>")
            sys.exit(1)
        public_key_file = sys.argv[2]
        master_key_file = sys.argv[3]
        attributes = sys.argv[4]
        private_key_file = sys.argv[5]
        gen_secret_key(cpabe, public_key_file, master_key_file, attributes, private_key_file)
        
    elif mode == 'encrypt':
        if len(sys.argv) < 5:
            print("Usage: python3 main.py encrypt <public_key_file> <plaintext_file with your policy> <ciphertext_file>")
            sys.exit(1)
        
        public_key_file = sys.argv[2]
        plaintext_file = sys.argv[3]
        ciphertext_file = sys.argv[4]
        with open(plaintext_file, 'r') as file:
            plaintext = file.read()

        encrypt_message(cpabe, public_key_file, plaintext_file, ciphertext_file)
    elif mode == 'decrypt':
        if len(sys.argv) < 6:
            print("Usage: python3 main.py decrypt <public_key_file> <private_key_file> <cipher_text_file> <recorvertext_file>")
            sys.exit(1)
        public_key_file = sys.argv[2]
        private_key_file = sys.argv[3]
        cipher_text_file = sys.argv[4]
        recorvertext_file = sys.argv[5]
        decrypt_message(cpabe, public_key_file, private_key_file, cipher_text_file, recorvertext_file)

    

if __name__ == "__main__":

    main()

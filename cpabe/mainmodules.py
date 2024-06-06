import argparse
from CPABE import CPABE
from charm.toolbox.pairinggroup import PairingGroup
from charm.core.engine.util import objectToBytes, bytesToObject

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

def generate_keys(cpabe):
    public_key, master_key = cpabe.ac17.setup()
    
    serialized_public_key = objectToBytes(public_key, cpabe.groupObj)
    serialized_master_key = objectToBytes(master_key, cpabe.groupObj)
    
    save_to_file(serialized_public_key, 'public_key.bin')
    save_to_file(serialized_master_key, 'master_key.bin')
    
    print("Keys generated and saved to 'public_key.bin' and 'master_key.bin'")

def encrypt_message(cpabe, attributes, policy, message):
    public_key = bytesToObject(load_from_file('public_key.bin'), cpabe.groupObj)
    
    user_attributes = attributes.split(',')
    encrypted_data = cpabe.AC17encrypt(public_key, message, policy)
    
    # Save the encrypted data to a file
    with open('encrypted_data.txt', 'w') as file:
        file.write(encrypted_data)
    
    print("Encrypted data saved to 'encrypted_data.txt'")

def decrypt_message(cpabe, attributes):
    public_key = bytesToObject(load_from_file('public_key.bin'), cpabe.groupObj)
    master_key = bytesToObject(load_from_file('master_key.bin'), cpabe.groupObj)
    
    user_attributes = attributes.split(',')
    private_key = cpabe.ac17.keygen(public_key, master_key, user_attributes)
    
    serialized_private_key = objectToBytes(private_key, cpabe.groupObj)
    save_to_file(serialized_private_key, 'private_key.bin')
    
    private_key = bytesToObject(load_from_file('private_key.bin'), cpabe.groupObj)

    # Load the encrypted data from the file
    with open('encrypted_data.txt', 'r') as file:
        encrypted_data = file.read()
    
    decrypted_message = cpabe.AC17decrypt(public_key, encrypted_data, private_key)
    if decrypted_message:
        print(f"Decrypted Message: {decrypted_message}")
        
        # Save the decrypted message to an output file
        with open('output.txt', 'w') as output_file:
            output_file.write(decrypted_message)
            
        print("Decrypted message saved to 'output.txt'")
    else:
        print("Decryption failed!")

def main(args):
    cpabe = CPABE("AC17")
    
    if args.mode == '1':
        generate_keys(cpabe)
    elif args.mode == '2':
        input_file = args.input_file
        with open(input_file, 'r') as file:
            message = file.read()
        attributes = args.attributes
        policy = args.policy
        encrypt_message(cpabe, attributes, policy, message)
    elif args.mode == '3':
        attributes = args.attributes
        decrypt_message(cpabe, attributes)
    else:
        print("Invalid mode. Please choose 1 for key generation, 2 for encryption, or 3 for decryption.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CP-ABE CLI Application")
    parser.add_argument("--input_file", type=str, required=False, help="Path to the input file")
    parser.add_argument("--mode", type=str, required=True, help="Mode of operation: 1 for key generation, 2 for encryption, 3 for decryption")
    parser.add_argument("--attributes", type=str, required=False, help="Attributes for encryption/decryption")
    parser.add_argument("--policy", type=str, required=False, help="Policy for encryption")

    args = parser.parse_args()
    main(args)

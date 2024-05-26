import sys
import os
import argparse
import base
import aesgcm

sys.path.append(os.getcwd())  # get current working dir and export to python paths
aesgcm = aesgcm.AES_GCM()
def generate_keys(args):
    columns = args.columns.split(',')
    aesgcm.gen_key(columns, args.keyfile, args.ivfile, args.csv_file)

def encrypt_data(args):
    columns = args.columns.split(',')
    cols = base.get_cols(args.plaintext_file)  # Extract columns from the CSV file
    aesgcm.encrypt_data(columns, cols, args.plaintext_file, args.keyfile, args.ivfile)


def decrypt_data(args):
    columns = args.columns.split(',')
    cols = base.get_cols(args.encrypted_file)  # Extract columns from the CSV file
    aesgcm.decrypt_data(columns, cols, args.encrypted_file, args.keyfile, args.ivfile)


def main():
    parser = argparse.ArgumentParser(description="Process encryption and decryption on CSV data.")
    subparsers = parser.add_subparsers()
    
    parser_genkey = subparsers.add_parser('genkey', help='Generate key and IV files')
    parser_genkey.add_argument('columns', type=str, help='Columns to generate keys for (comma-separated or "all")')
    parser_genkey.add_argument('keyfile', type=str, help='Path to the key file')
    parser_genkey.add_argument('ivfile', type=str, help='Path to the IV file')
    parser_genkey.add_argument('--csv_file', type=str, help='Path to the CSV file (required if "all" is specified)')
    parser_genkey.set_defaults(func=generate_keys)


    parser_encrypt = subparsers.add_parser('encrypt', help='Encrypt data')
    parser_encrypt.add_argument('columns', type=str, help='Columns to encrypt (comma-separated or "all")')
    parser_encrypt.add_argument('plaintext_file', type=str, help='Path to the plaintext CSV file')
    parser_encrypt.add_argument('keyfile', type=str, help='Path to the key file')
    parser_encrypt.add_argument('ivfile', type=str, help='Path to the IV file')
    parser_encrypt.set_defaults(func=encrypt_data)

    parser_decrypt = subparsers.add_parser('decrypt', help='Decrypt data')
    parser_decrypt.add_argument('columns', type=str, help='Columns to decrypt (comma-separated or "all")')
    parser_decrypt.add_argument('encrypted_file', type=str, help='Path to the encrypted CSV file')
    parser_decrypt.add_argument('keyfile', type=str, help='Path to the key file')
    parser_decrypt.add_argument('ivfile', type=str, help='Path to the IV file')
    parser_decrypt.set_defaults(func=decrypt_data)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
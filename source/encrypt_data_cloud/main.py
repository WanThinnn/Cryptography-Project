import sys, os, time, csv, base64, binascii
import base, aesgcm, user
import argparse
sys.path.append(os.getcwd()) # get curent working dir and export to python paths
from mypackages import key_expansion,modes

aesgcm = aesgcm.AES_GCM()
def generate_keys(args):
    tables, tables_path = base.process_database()
    cols = base.get_cols(tables_path)

    aesgcm.gen_key(len(cols), tables)

def encrypt_data(args):
    tables, tables_path = base.process_database()
    cols = base.get_cols(tables_path)
    keys_file = input()
    ivs_file = input()
    choices = args.columns.split(',')
    aesgcm.encrypt_data(choices, cols, tables, keys_file, ivs_file, args.plaintext_file)

def decrypt_data(args):
    tables, tables_path = base.process_database()
    cols = base.get_cols(tables_path)
    keys_list = base.read_keys_from_file(f"keys_{tables}.txt")
    ivs_list = base.read_ivs_from_file(f"ivs_{tables}.txt")

    mode_map = base.create_mode_map(cols)

    choices = args.columns.split(',')

    aesgcm.decrypt_data(choices, mode_map, cols, tables, keys_list, ivs_list, args.encrypted_file)

def main():
    parser = argparse.ArgumentParser(description="Process encryption and decryption on CSV data.")
    subparsers = parser.add_subparsers()

    parser_genkey = subparsers.add_parser('genkey', help='Generate keys')
    parser_genkey.set_defaults(func=generate_keys)

    parser_encrypt = subparsers.add_parser('encrypt', help='Encrypt data')
    parser_encrypt.add_argument('columns', type=str, help='Columns to encrypt (comma-separated)')
    parser_encrypt.add_argument('plaintext_file', type=str, help='Path to the plaintext CSV file')
    parser_encrypt.set_defaults(func=encrypt_data)

    parser_decrypt = subparsers.add_parser('decrypt', help='Decrypt data')
    parser_decrypt.add_argument('columns', type=str, help='Columns to decrypt (comma-separated)')
    parser_decrypt.add_argument('encrypted_file', type=str, help='Path to the encrypted CSV file')
    parser_decrypt.set_defaults(func=decrypt_data)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()





# aesgcm = aesgcm.AES_GCM()
# def process(plaintext_csv_path, tables, keys_list, ivs_list, tables_path, cols, mode):

#     # Lựa chọn chế độ
#     print("Chọn chế độ:")
#     print("1. Tạo key:")
#     print("2. Mã hoá:")
#     print("3. Giải mã:")
#     print("4. Thoát:")
#     mode = int(input("Chọn: "))
#     print()


#     # Kiểm tra xem lựa chọn có hợp lệ không và gọi hàm tương ứng
#     if mode == 1:
#         num_columns = len(cols)
#         aesgcm.gen_key(num_columns, tables)

        
#     elif mode == 2:
#         mode_map = base.create_mode_map(cols)
#         base.print_cols(cols)
#         choice_str = input("Chọn (cách nhau 1 dấu phẩy nếu chọn nhiều hơn 1): ")
#         choices = choice_str.split(',')
#         start_time = time.time()
#         aesgcm.encrypt_data(choices, mode_map, cols, tables, keys_list, ivs_list, plaintext_csv_path)
#         end_time = time.time()
#         execution_time = round(end_time - start_time,2)
#         print(f"Thời gian thực thi: {execution_time} giây\n")
#     elif mode == 3:
#         encrypted_csv_path = input("Encrypted data csv file: ")
#         mode_map = base.create_mode_map(cols)
#         base.print_cols(cols)
#         choice_str = input("Chọn (cách nhau 1 dấu phẩy nếu chọn nhiều hơn 1): ")
#         choices = choice_str.split(',')
#         start_time = time.time()
#         aesgcm.decrypt_data(choices, mode_map, cols, tables, keys_list, ivs_list, encrypted_csv_path)
#         end_time = time.time()
#         execution_time = round(end_time - start_time,2)
#         print(f"Thời gian thực thi: {execution_time} giây\n")
#     elif mode == 4:
#         print(f"Kết thúc phiên làm việc với bảng {tables}\n")

#     else:
#         print("Lựa chọn không hợp lệ.\n")

# tables, tables_path = base.process_database()
# cols = base.get_cols(tables_path)

# plaintext_csv_path = input("Plaintext data csv file: ")
# print(tables)
# print(tables_path)


# keys_list = base.read_keys_from_file(f"keys_{tables}.txt")
# ivs_list = base.read_ivs_from_file(f"ivs_{tables}.txt")

# process(plaintext_csv_path, tables, keys_list, ivs_list, tables_path, cols, 1)

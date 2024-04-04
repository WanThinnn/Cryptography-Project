# -*- coding: utf-8 -*-
#Ref: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197-upd1.pdf
# Mode: https://csrc.nist.gov/pubs/sp/800/38/a/sup/final
import sys, os
sys.path.append(os.getcwd()) # get curent working dir and export to python paths
from mypackages import key_expansion,modes

import csv
import base64
import binascii
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Convert text <--> bin
def message_to_bin(message):
    """Convert a string message to its binary representation using UTF-8 encoding."""
    binary_message = ''.join(format(byte, '08b') for byte in message.encode('utf-8'))
    return binary_message

def hex_to_base64(hex_string):
    hex_bytes = bytes.fromhex(hex_string)
    base64_bytes = base64.b64encode(hex_bytes)
    return base64_bytes.decode('utf-8')

def base64_to_hex(base64_string):
    decoded_bytes = base64.b64decode(base64_string)
    hex_string = binascii.hexlify(decoded_bytes).decode('utf-8')
    return hex_string

def generate_keys(cols):
    num_columns = len(cols)
    keys = {}
    for i in range(num_columns):
        key = get_random_bytes(16) 
        keys[i] = key
    print("Tạo key thành công!")
    return keys

def save_keys_to_file(keys, file_path):
    with open(file_path, 'w') as file:
        for key in keys.values():  # Lặp qua các giá trị của từ điển keys
            key_hex = key.hex()  # Chuyển đổi key thành dạng hex
            file.write(f"{key_hex}\n")

def read_keys_from_file(file_path):
    keys = []
    with open(file_path, 'r') as file:
        for line in file:
            # Tách tên key và giá trị key từ mỗi dòng
            key_value = line.strip()
            # Thêm key vào danh sách keys
            keys.append(key_value)
    return keys

def get_cols(csv_file_path):
    cols = []
    # Đọc dòng đầu tiên của file CSV và lưu vào mảng cols
    with open(csv_file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        cols = next(reader)  # Đọc dòng đầu tiên và lưu vào mảng cols
    return cols

def get_tables(file_path):
    result = []  # Khởi tạo một list để lưu trữ các hàng từ file CSV
    with open(file_path, 'r') as file:
        # Đọc từng dòng của file văn bản
        for line in file:
            # Xử lý dòng là một bảng CSV
                result.append(line.strip())  # Thêm dòng sau khi loại bỏ dấu xuống dòng vào mảng
    return result

def print_cols(cols):
    print('Mời nhập cột cần xử lý: ')
    # In ra tên các cột
    for i, col in enumerate(cols, start=1):
        print(f"{i}. {col}")

def print_tables(tables):
    print('Mời nhập bảng cần xử lý: ')
    for i, table in enumerate(tables, start=1):
        print(f"{i}. {table}")
    
def create_mode_map(cols):
    mode_map = {}
    for i, col in enumerate(cols, start=1):
        mode_map[str(i)] = col
    mode_map[str(len(cols) + 1)] = "all_data"
    return mode_map


def select_csv_file(database):
    tables = get_tables(database)
    print_tables(tables)
    choice = int(input("Chọn: "))
    if (choice > len(tables)) or (choice < 1):
        print("Lỗi, nhập lại!")
        sys.exit()  # Kết thúc chương trình nếu có lỗi
    return tables[choice-1]

def encrypt(plaintext, key256):
    key_bytes_256 = key256.encode('utf-8')
    aes_mode = modes.modes(key_bytes_256)
    cipher = aes_mode.cbc_encrypt(plaintext)
    return hex_to_base64(cipher.hex())

def dencrypt(ciphertext, key256):
    key_bytes_256 = key256.encode('utf-8')
    aes_mode = modes.modes(key_bytes_256)
    decrypt_function = aes_mode.cbc_decrypt
    ciphertext_hex = base64_to_hex(ciphertext)
    ciphertext_bytes = bytes.fromhex(ciphertext_hex)
    return decrypt_function(ciphertext_bytes)
    
def Ma_hoa(cols, key_list, plaintext_csv_path, encrypted_csv_path):

    with open(plaintext_csv_path, 'r', newline='') as input_file,\
            open(encrypted_csv_path, 'w', newline='') as output_file:
        
        reader = csv.DictReader(input_file)
        fieldnames = reader.fieldnames  # Lấy tên cột

        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            for i in range(len(cols)):
                row[cols[i]] = encrypt(row[cols[i]], keys_list[i])
                # row[cols[i]] = hex_to_base64(row[cols[i]])
            # Ghi hàng đã mã hóa vào tệp CSV mới
            writer.writerow(row)
        print("Mã hoá toàn bộ dữ liệu thành công!")
    
def Giai_ma(choice, mode_map, cols, tables, keys_list, encrypted_csv_path):
    chosen_column = mode_map.get(choice)  # Lấy giá trị tương ứng với lựa chọn của người dùng
    choose = mode_map.get(choice)
    
    if chosen_column not in mode_map.values():
        print("Lựa chọn không hợp lệ.")
        return
    else:
        i = int(choice) - 1  # Định nghĩa giá trị của biến i dựa trên lựa chọn của người dùng
        print("Bạn đã chọn cột:", chosen_column)

    decrypted_data = []
    
    try:
        if (i == 7):
            with open(encrypted_csv_path, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    decrypted_row = {}  # Tạo một hàng mới để lưu trữ các giá trị giải mã
                    for j, col in enumerate(cols):  # Duyệt qua mỗi cột và giải mã giá trị tương ứng
                        # ciphertext_hex = base64_to_hex(row[col])
                        plaintext = dencrypt(ciphertext_hex, keys_list[j])
                        decrypted_row[col] = plaintext  # Thêm giá trị giải mã vào hàng mới

                    decrypted_data.append(decrypted_row)  # Thêm hàng đã giải mã vào danh sách
                # Đường dẫn đến file CSV đã giải mã
            
            decrypted_csv_path = f"dencrypted_{tables}_{choose}.csv"

            # Viết dữ liệu đã giải mã vào file CSV mới
            with open(decrypted_csv_path, 'w', newline='') as csvfile:
                fieldnames = decrypted_data[0].keys()  # Sử dụng keys của bất kỳ hàng nào để lấy tên cột
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(decrypted_data)
            print(f"Giải mã thành công! Dữ liệu giải mã '{choose}' được lưu tại '{decrypted_csv_path}'.")
            
        else:
            with open(encrypted_csv_path, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    ciphertext_hex = row[choose]
                    plaintext = dencrypt(ciphertext_hex, keys_list[i])
                    row[choose] = plaintext
                    decrypted_data.append(row)

            # Đường dẫn đến file CSV đã giải mã
            decrypted_csv_path = f"dencrypted_{tables}_{choose}.csv"

            # Viết dữ liệu đã giải mã vào file CSV mới
            with open(decrypted_csv_path, 'w', newline='') as csvfile:
                fieldnames = decrypted_data[0].keys()  # Sử dụng keys của bất kỳ hàng nào để lấy tên cột
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(decrypted_data)
            print(f"Giải mã thành công! Dữ liệu giải mã '{choose}' được lưu tại '{decrypted_csv_path}'.")
            
            
    except ValueError:
        print ("Giải mã thất bại! Sai khoá hoặc lỗi!" ) # Thông báo khi khoá không chính xác



switch_case = {
    1: generate_keys,
    2: Ma_hoa,  # Đây chỉ là tên hàm, không gọi ngay lập tức
    3: Giai_ma  # Đây cũng chỉ là tên hàm, không gọi ngay lập tức
}


tables = select_csv_file("database.txt")
tables_path = f"{tables}.csv"

# Lựa chọn chế độ
print("Chọn chế độ:")
print("1. Tạo key:")
print("2. Mã hoá:")
print("3. Giải mã:")
mode = int(input("Chọn: "))

# Kiểm tra xem lựa chọn có hợp lệ không và gọi hàm tương ứng
if mode == 1:
    cols = get_cols(tables_path)
    keys = generate_keys(cols)
    save_keys_to_file(keys, f"keys_{tables}.txt")
elif mode == 2:
    cols = get_cols(tables_path)
    keys_list = read_keys_from_file(f"keys_{tables}.txt")
    encrypted_csv_path = f"encrypted_{tables}.csv"
    Ma_hoa(cols, keys_list, tables_path, encrypted_csv_path)
    
elif mode == 3:
    keys_list = read_keys_from_file(f"keys_{tables}.txt")
    encrypted_csv_path = f"encrypted_{tables}.csv"
    cols = get_cols(tables_path)
    mode_map = create_mode_map(cols)
    print_cols(cols)
    choice = input("Enter choice: ")
    Giai_ma(choice, mode_map, cols, tables, keys_list, encrypted_csv_path)
else:
    print("Lựa chọn không hợp lệ.")

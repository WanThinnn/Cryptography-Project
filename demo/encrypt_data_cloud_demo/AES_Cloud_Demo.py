# -*- coding: utf-8 -*-
#Ref: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197-upd1.pdf
# Mode: https://csrc.nist.gov/pubs/sp/800/38/a/sup/final
import sys, os
sys.path.append(os.getcwd()) # get curent working dir and export to python paths
from mypackages import key_expansion,modes

import csv
import binascii
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Convert text <--> bin
def message_to_bin(message):
    """Convert a string message to its binary representation using UTF-8 encoding."""
    binary_message = ''.join(format(byte, '08b') for byte in message.encode('utf-8'))
    return binary_message


def generate_keys(num_columns):
    keys = {}
    for i in range(num_columns):
        key = get_random_bytes(16)  # Tạo một key ngẫu nhiên có độ dài 16 bytes (128 bits)
        # key_bytes_128 = key.encode('utf-8')
        keys[f'key_{i+1}'] = key
    return keys

def save_keys_to_file(keys, file_path):
    with open(file_path, 'w') as file:
        for key_name, key in keys.items():
            key_hex = key.hex()
            file.write(f"{key_name}: {key_hex}\n")

def read_keys_from_file(file_path):
    keys = []
    with open(file_path, 'r') as file:
        for line in file:
            # Tách tên key và giá trị key từ mỗi dòng
            key_value = line.strip()
            # Thêm key vào danh sách keys
            keys.append(key_value)
    return keys

def encrypt(plaintext, key128):
    keys_list = read_keys_from_file('keys.txt')
    # key128 = "12345678abcdefgh"
    key_bytes_128 = key128.encode('utf-8')
    aes_mode = modes.modes(key_bytes_128)
    cipher = aes_mode.cbc_encrypt(plaintext)
    return cipher.hex()

    


def dencrypt(ciphertext_hex, key128):
    key_bytes_128 = key128.encode('utf-8')  # Chuyển đổi key sang dạng bytes
    aes_mode = modes.modes(key_bytes_128)
    decrypt_function = aes_mode.cbc_decrypt
    ciphertext_bytes = bytes.fromhex(ciphertext_hex)  # Chuyển đổi ciphertext từ dạng hex sang dạng bytes
    return decrypt_function(ciphertext_bytes)
    


def Ma_hoa():
    # Số lượng cột trong file CSV
    # num_columns = 7
    # Tạo keys cho mỗi cột
    # keys = generate_keys(num_columns)
    # Lưu keys vào file .txt
    # save_keys_to_file(keys, 'keys.txt')
    cols = ["id", "name", "type" ,"import_date" ,"price","public_date","manager_id"]
    keys_list = read_keys_from_file('keys.txt')
    plaintext_csv_path = "plaintext.csv"
    encrypted_csv_path = "encrypted_data.csv"
    
    with open(plaintext_csv_path, 'r', newline='') as input_file,\
            open(encrypted_csv_path, 'w', newline='') as output_file:
        
        reader = csv.DictReader(input_file)
        fieldnames = reader.fieldnames  # Lấy tên cột

        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            for i in range(len(cols)):
                row[cols[i]] = encrypt(row[cols[i]], keys_list[i])
                # Ghi hàng đã mã hóa vào tệp CSV mới
            writer.writerow(row)
        print("Encryption completed.")
    

def Giai_ma():
    print('Moi nhap cot can giai ma: ')
    print("1. id")
    print("2. name")
    print("3. type")
    print("4. import_date")
    print("5. price")
    print("6. public_date")
    print("7. manager_id")
    choice = input("Enter choice (1/2/3/4/5/6/7): ")
    mode_map = {
        "1": "id",
        "2": "name",
        "3": "type",
        "4": "import_date",
        "5": "price",
        "6": "public_date",
        "7": "manager_id"
        
    }
    chosen_column = mode_map.get(choice)  # Lấy giá trị tương ứng với lựa chọn của người dùng
    choose = mode_map.get(choice)
    if chosen_column not in mode_map.values():
        print("Lựa chọn không hợp lệ.")
        return
    else:
        i = int(choice) - 1  # Định nghĩa giá trị của biến i dựa trên lựa chọn của người dùng
        print("Bạn đã chọn cột:", chosen_column)


    keys_list = read_keys_from_file('keys.txt')
    
    # Đường dẫn đến file CSV đã mã hóa
    encrypted_csv_path = "encrypted_data.csv"

    # Đọc dữ liệu từ file CSV đã mã hóa
    decrypted_data = []
    try:
        with open(encrypted_csv_path, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                ciphertext_hex = row[choose]
                plaintext = dencrypt(ciphertext_hex, keys_list[i])
                row[choose] = plaintext
                decrypted_data.append(row)

        # Đường dẫn đến file CSV đã giải mã
        decrypted_csv_path = f"dencrypted_{choose}.csv"

        # Viết dữ liệu đã giải mã vào file CSV mới
        with open(decrypted_csv_path, 'w', newline='') as csvfile:
            fieldnames = decrypted_data[0].keys()  # Sử dụng keys của bất kỳ hàng nào để lấy tên cột
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(decrypted_data)
        print(f"Decrypted data for column '{choose}' saved to '{decrypted_csv_path}'.")
    except ValueError:
        print ("Decryption failed: Incorrect key!" ) # Thông báo khi khoá không chính xác








switch_case = {
    1: Ma_hoa,  # Đây chỉ là tên hàm, không gọi ngay lập tức
    2: Giai_ma  # Đây cũng chỉ là tên hàm, không gọi ngay lập tức
}

# Lựa chọn chế độ
mode = int(input("Chọn chế độ:\n1. Mã hóa\n2. Giải mã\nChọn: "))

# Kiểm tra xem lựa chọn có hợp lệ không và gọi hàm tương ứng
if mode in switch_case:
    switch_case[mode]()  # Gọi hàm tương ứng với lựa chọn
else:
    print("Lựa chọn không hợp lệ.")


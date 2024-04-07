import sys, os, time, csv, base64, binascii
sys.path.append(os.getcwd()) # get curent working dir and export to python paths
from mypackages import key_expansion,modes


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
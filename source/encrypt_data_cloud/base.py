import sys, os, time, csv, base64, binascii
from cryptography.hazmat.primitives.ciphers import (Cipher, algorithms, modes)

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
    i = 1
    for i, col in enumerate(cols, start=1):
        print(f"{i}. {col}")
    print(f"{i+1}. all_data")

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
    print(f"{len(tables)+1}. Thoát")  # Thêm tuỳ chọn "Thoát"
    
    choice = int(input("Chọn: "))
    print()
    if choice == len(tables)+1:
        sys.exit()  # Thoát chương trình nếu người dùng chọn "Thoát"
    elif (choice > len(tables)+1) or (choice < 1):
        print("Lỗi, nhập lại!")
        sys.exit()  # Kết thúc chương trình nếu có lỗi
    return tables[choice-1]

def save_keys_to_file(keys, file_path):
    with open(file_path, 'w') as file:
        for key in keys:  # Lặp qua các giá trị của từ điển keys
            key_hex = key.hex()  # Chuyển đổi key thành dạng hex
            file.write(f"{key_hex}\n")

def read_keys_from_file(file_path):
    keys = []
    with open(file_path, 'r') as file:
        for line in file:
            # Tách tên key và giá trị key từ mỗi dòng
            key_bytes = bytes.fromhex(line.strip())
            # Thêm key vào danh sách keys
            keys.append(key_bytes)
    return keys


# def encrypt(plaintext, key256, nonce, aad):
#     aesgcmsiv = AESGCMSIV(key256)
#     ciphertext = aesgcmsiv.encrypt(nonce, plaintext.encode('utf-8'), aad.encode('utf-8'))  # Encode plaintext to bytes
#     return ciphertext

def encrypt(key, plaintext, associated_data):
    # Generate a random 96-bit IV.
    iv = os.urandom(12)

    # Construct an AES-GCM Cipher object with the given key and a
    # randomly generated IV.
    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
    ).encryptor()

    # associated_data will be authenticated but not encrypted,
    # it must also be passed in on decryption.
    encryptor.authenticate_additional_data(associated_data)

    # Encrypt the plaintext and get the associated ciphertext.
    # GCM does not require padding.
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    return (iv, ciphertext, encryptor.tag)

# def decrypt(ciphertext, key256, nonce, aad):
#     aesgcmsiv = AESGCMSIV(key256)
#     decrypted_data = aesgcmsiv.decrypt(nonce, ciphertext, aad.encode('utf-8'))
#     return decrypted_data.decode('utf-8')


def decrypt(key, associated_data, iv, ciphertext, tag):
    # Construct a Cipher object, with the key, iv, and additionally the
    # GCM tag used for authenticating the message.
    decryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag),
    ).decryptor()

    # We put associated_data back in or the tag will fail to verify
    # when we finalize the decryptor.
    decryptor.authenticate_additional_data(associated_data)

    # Decryption gets us the authenticated plaintext.
    # If the tag does not match an InvalidTag exception will be raised.
    return decryptor.update(ciphertext) + decryptor.finalize()



def login():
    username = input("Username: ")
    password = input("Password: ")

    # Kiểm tra thông tin đăng nhập
    if username == "admin" and password == "123":
        print("Đăng nhập thành công!\n")
        return "admin"
    elif username == "user" and password == "123":
        print("Đăng nhập thành công!\n")
        return "user"
    else:
        print("Sai tên người dùng hoặc mật khẩu.")
        return None
    
    

def process_database():
    tables = select_csv_file("database.txt")
    tables_path = f"{tables}.csv"
    return tables, tables_path
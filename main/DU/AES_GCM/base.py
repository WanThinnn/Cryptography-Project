import sys, os, time, csv, base64, binascii
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

sys.path.append(os.getcwd()) # get curent working dir and export to python paths



def ByteToBase64(byte_text):
    return base64.b64encode(byte_text).decode('utf-8')

def Base64ToByte(byte_text):
    return base64.b64decode(byte_text)

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


# def get_cols(csv_file_path):
#     cols = []
#     # Đọc dòng đầu tiên của file CSV và lưu vào mảng cols
#     with open(csv_file_path, 'r', newline='') as csvfile:
#         reader = csv.reader(csvfile)
#         cols = next(reader)  # Đọc dòng đầu tiên và lưu vào mảng cols
#     return cols
def get_cols(csv_file):
    with open(csv_file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        return next(reader)  # Return the header row as a list of column names

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

def save_keys_to_file(keys, keyfile):
    with open(keyfile, 'w') as f:
        f.write("columns, key\n")
        for column, key in keys.items():
            f.write(f"{column}, {key}\n")
            
def save_keys_iv_to_file(key_iv_pairs, keyivfile):
    with open(keyivfile, 'w') as f:
        f.write("columns,key\n")
        for column, key_iv in key_iv_pairs.items():
            f.write(f"{column},{key_iv}\n")


def save_ivs_to_file(ivs, ivfile):
    with open(ivfile, 'w') as f:
        f.write("columns,iv\n")
        for column, iv in ivs.items():
            f.write(f"{column},{iv}\n")

def read_key_iv_from_file(key_iv_file):
        key_iv_dict = {}
        with open(key_iv_file, 'r') as f:
            next(f)  # Skip the header
            for line in f:
                column, key_iv = line.strip().split(', ')
                key_iv_dict[column] = key_iv
        return key_iv_dict

def read_keys_from_file(keyfile):
    keys = {}
    with open(keyfile, 'r') as f:
        next(f)  # Skip the header
        for line in f:
            column, key = line.strip().split(', ')
            keys[column] = key
    return keys

def read_ivs_from_file(ivfile):
    ivs = {}
    with open(ivfile, 'r') as f:
        next(f)  # Skip the header
        for line in f:
            column, iv = line.strip().split(', ')
            ivs[column] = iv
    return ivs


def login():
    return "admin"
    # username = input("Username: ")
    # password = input("Password: ")

    # # Kiểm tra thông tin đăng nhập
    # if username == "admin" and password == "123":
    #     print("Đăng nhập thành công!\n")
    #     return "admin"
    # elif username == "user" and password == "123":
    #     print("Đăng nhập thành công!\n")
    #     return "user"
    # else:
    #     print("Sai tên người dùng hoặc mật khẩu.")
    #     return None
    
    

def process_database():
    tables = select_csv_file("/Users/wanthinnn/Documents/Cryptography/Cryptography-Project/source/database.txt")
    tables_path = f"{tables}.csv"
    return tables, tables_path
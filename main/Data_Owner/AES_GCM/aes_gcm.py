
import sys
import os

# Lấy đường dẫn hiện tại của tệp đang chạy
current_dir = os.path.dirname(os.path.abspath(__file__))

# Lấy đường dẫn của thư mục cha
parent_dir = os.path.dirname(current_dir)

# Thêm đường dẫn của thư mục cha vào sys.path
sys.path.append(parent_dir)

import base
import time, csv, base64, binascii
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
sys.path.append(os.getcwd()) # get curent working dir and export to python paths

class AES_GCM:    

    def __init__(self):
        pass

    def save_dec_data_to_csv(self):
        # Viết dữ liệu đã giải mã vào file CSV mới
        with open(self.decrypted_csv_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.decrypted_data.keys())
            writer.writeheader()

            # Sử dụng zip để kết hợp dữ liệu từ các cột thành các hàng
            for row in zip(*self.decrypted_data.values()):
                writer.writerow(dict(zip(self.decrypted_data.keys(), row)))
                
    def save_enc_data_to_csv(self):
        # Viết dữ liệu đã giải mã vào file CSV mới
        with open(self.encrypted_csv_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.encrypted_data.keys())
            writer.writeheader()

            # Sử dụng zip để kết hợp dữ liệu từ các cột thành các hàng
            for row in zip(*self.encrypted_data.values()):
                writer.writerow(dict(zip(self.encrypted_data.keys(), row))) 
                

    def gen_key(self, columns, keyfile):
        key_iv_pairs = {}

        for column in columns:
            iv = os.urandom(12)  # Tạo IV ngẫu nhiên 12 bytes
            key = os.urandom(32)  # Tạo key ngẫu nhiên 32 bytes
            key_iv_pairs[column] = base.ByteToBase64(key + iv)

        base.save_keys_iv_to_file(key_iv_pairs, keyfile)

        print("Tạo key và IV thành công cho các cột!")

    # Hàm mã hóa sử dụng AES GCM
    def encrypt(self, plaintext, key_iv):
        key_iv_bytes = base.Base64ToByte(key_iv)
        key = key_iv_bytes[:32]
        iv = key_iv_bytes[32:44]
        aesgcm = AESGCM(key)
        plaintext_bytes = plaintext.encode('utf-8')
        ciphertext_with_tag = aesgcm.encrypt(iv, plaintext_bytes, None)
        ciphertext = base.ByteToBase64(ciphertext_with_tag)
        return ciphertext

    # Hàm giải mã sử dụng AES GCM
    def decrypt(self, ciphertext, key_iv):
        key_iv_bytes = base.Base64ToByte(key_iv)
        key = key_iv_bytes[:32]
        iv = key_iv_bytes[32:44]
        ciphertext = base.Base64ToByte(ciphertext)
        aesgcm = AESGCM(key)
        recovertext_bytes = aesgcm.decrypt(iv, ciphertext, None)
        recovertext = recovertext_bytes.decode('utf-8')
        return recovertext
    
    

    def encrypt_data(self, encrypted_csv_path, selected_columns, cols, plaintext_file, key_iv_file):
        key_iv_dict = base.read_key_iv_from_file(key_iv_file)

        # If 'all' is specified in choices, replace it with all columns
        if 'all' in selected_columns:
            selected_columns = cols

        try:
            with open(plaintext_file, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                with open(encrypted_csv_path, 'w', newline='') as output_file:
                    writer = csv.DictWriter(output_file, fieldnames=reader.fieldnames)
                    writer.writeheader()

                    for row in reader:
                        encrypted_row = row.copy()
                        for choice in selected_columns:
                            if choice in row:
                                plaintext = row[choice]
                                if choice in key_iv_dict:
                                    try:
                                        ciphertext = self.encrypt(plaintext, key_iv_dict[choice])
                                        encrypted_row[choice] = ciphertext
                                    except Exception as e:
                                        print(f"Mã hóa thất bại cho cột {choice}: {e}")
                                else:
                                    print(f"Không tìm thấy key và IV cho cột {choice}")
                        writer.writerow(encrypted_row)
        
        except Exception as e:
            print(f"Đã xảy ra lỗi: {e}")

        print(f"Mã hóa thành công! Dữ liệu mã hóa được lưu tại '{encrypted_csv_path}'!")



    def decrypt_data(self, decrypted_csv_path, selected_columns, cols, encrypted_csv_path, keys_file):

            key_iv_dict = base.read_key_iv_from_file(keys_file)
            
            # If 'all' is specified in choices, replace it with all columns
            if 'all' in selected_columns:
                selected_columns = cols

            try:
                with open(encrypted_csv_path, 'r', newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    with open(decrypted_csv_path, 'w', newline='') as output_file:
                        writer = csv.DictWriter(output_file, fieldnames=reader.fieldnames)
                        writer.writeheader()

                        for row in reader:
                            decrypted_row = row.copy()
                            for choice in selected_columns:
                                if choice in row:
                                    ciphertext_base64 = row[choice]
                                    if choice in key_iv_dict:
                                        try:
                                            recovertext = self.decrypt(ciphertext_base64, key_iv_dict[choice])
                                            decrypted_row[choice] = recovertext
                                        except Exception as e:
                                            print(f"Giải mã thất bại cho cột {choice}: {e}")
                                    else:
                                        return
                            writer.writerow(decrypted_row)
            
            except ValueError as e:
                return

            print(f"Giải mã thành công! Dữ liệu giải mã được lưu tại '{decrypted_csv_path}'!\n")

   

    
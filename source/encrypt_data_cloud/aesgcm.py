

import base
import sys, os, time, csv, base64, binascii
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
sys.path.append(os.getcwd()) # get curent working dir and export to python paths
from mypackages import key_expansion,modes

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
                
    def gen_key(self, num_columns, tables):
        
        self.keys = []
        self.ivs = []
        for i in range(num_columns):
            iv = base.ByteToBase64(os.urandom(12))  # Tạo nonce ngẫu nhiên 16 bytes
            key = base.ByteToBase64(os.urandom(32))  # AES-256
            self.keys.append(key)
            self.ivs.append(iv)
                        
        base.save_keys_to_file(self.keys, f"keys_{tables}.txt")
        base.save_ivs_to_file(self.ivs, f"ivs_{tables}.txt")
        print("Tạo key thành công!\n")
    # Hàm mã hóa sử dụng AES GCM
    def encrypt(plaintext, key, IV):
        aesgcm = AESGCM(key)
        plaintext_bytes = plaintext.encode('utf-8')
        ciphertext_with_tag = aesgcm.encrypt(IV, plaintext_bytes, None)
        ciphertext = base.ByteToBase64(ciphertext_with_tag)
        return ciphertext

    # Hàm giải mã sử dụng AES GCM
    def decrypt(ciphertext, key, IV):
        ciphertext = base.Base64ToByte(ciphertext)
        aesgcm = AESGCM(key)
        recovertext_bytes = aesgcm.decrypt(IV, ciphertext, None)
        recovertext = recovertext_bytes.decode('utf-8')
        return recovertext
    
    def encrypt_data(self, choices, cols, tables, keys_file, ivs_file, plaintext_csv_path):
        
        self.name_file = input('Đặt tên file: ')
        self.encrypted_csv_path = f"encrypted_{tables}_{self.name_file}.csv"
        # Khởi tạo từ điển để lưu trữ dữ liệu mã hóa
        self.encrypted_data = {}
        keys_list = base.read_keys_from_file(keys_file)
        ivs_list = base.read_ivs_from_file(ivs_file)
        mode_map = base.create_mode_map(cols)
        
        try:
            with open(plaintext_csv_path, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)

                with open(self.encrypted_csv_path, 'w', newline='') as output_file:
                    writer = csv.DictWriter(output_file, fieldnames=reader.fieldnames)
                    writer.writeheader()

                    for row in reader:
                        for index, choice in enumerate(choices):
                            chosen_column = mode_map.get(choice)  # Lấy giá trị tương ứng với lựa chọn của người dùng

                            # Mã hoá dữ liệu cho cột được chọn
                            if self.chosen_column == "all_data"  and len(choices) == 1:
                                for j, col in enumerate(cols):  # Duyệt qua mỗi cột và giải mã giá trị tương ứng
                                    self.plaintext = (row[col])
                                    self.ciphertext = self.encrypt(self.ciphertext_base64, keys_list[j], ivs_list[j])
                                    # Lưu dữ liệu giải mã vào từ điển
                                    if col not in self.encrypt_data:
                                        self.decrypted_data[col] = []
                                    self.decrypted_data[col].append(self.ciphertext)
                            else:
                                i = cols.index(self.chosen_column)
                                self.ciphertext_base64 = (row[self.chosen_column])
                                self.recovertext = self.decrypt(self.ciphertext_base64, keys_list[i], ivs_list[i])
                                # Lưu dữ liệu giải mã vào từ điển
                                if self.chosen_column not in self.decrypted_data:
                                    self.decrypted_data[self.chosen_column] = []
                                self.decrypted_data[self.chosen_column].append(self.recovertext)

        except ValueError:
            print("Mã hoá thất bại! Sai khóa hoặc lỗi!")
                    # Lưu dữ liệu giải mã vào file CSV
        self.save_enc_data_to_csv()
        print(f"Mã hoá thành công! Dữ liệu mã hoá được lưu tại '{self.encrypted_csv_path}'!")


            

    def decrypt_data(self, choices, mode_map, cols, tables, keys_file, ivs_file, encrypted_csv_path):
        self.name_file = input('Đặt tên file: ')
        self.decrypted_csv_path = f"dencrypted_{tables}_{self.name_file}.csv"
        keys_list = base.read_keys_from_file(keys_file)
        ivs_list = base.read_ivs_from_file(ivs_file)
        # Khởi tạo từ điển để lưu trữ dữ liệu giải mã
        self.decrypted_data = {}
        for index, choice in enumerate(choices):
            self.chosen_column = mode_map.get(choice)  # Lấy giá trị tương ứng với lựa chọn của người dùng

            if self.chosen_column not in mode_map.values():
                print("Lựa chọn không hợp lệ.\n")
                return
            else:
                print("Bạn đã chọn giải mã:", self.chosen_column)
        try:
            with open(encrypted_csv_path, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    for index, choice in enumerate(choices):
                        self.chosen_column = mode_map.get(choice)  # Lấy giá trị tương ứng với lựa chọn của người dùng

                        # Giải mã dữ liệu cho cột được chọn
                        if self.chosen_column == "all_data"  and len(choices) == 1:
                            for j, col in enumerate(cols):  # Duyệt qua mỗi cột và giải mã giá trị tương ứng
                                self.ciphertext_base64 = (row[col])
                                self.recovertext = self.decrypt(self.ciphertext_base64, keys_list[j], ivs_list[j])
                                # Lưu dữ liệu giải mã vào từ điển
                                if col not in self.decrypted_data:
                                    self.decrypted_data[col] = []
                                self.decrypted_data[col].append(self.recovertext)
                        else:
                            i = cols.index(self.chosen_column)
                            self.ciphertext_base64 = (row[self.chosen_column])
                            self.recovertext = self.decrypt(self.ciphertext_base64, keys_list[i], ivs_list[i])
                            # Lưu dữ liệu giải mã vào từ điển
                            if self.chosen_column not in self.decrypted_data:
                                self.decrypted_data[self.chosen_column] = []
                            self.decrypted_data[self.chosen_column].append(self.recovertext)

        except ValueError:
            print("Giải mã thất bại! Sai khoá hoặc lỗi!\n")  # Thông báo khi khoá không chính xác
            return

        # Lưu dữ liệu giải mã vào file CSV
        self.save_dec_data_to_csv()

        print(f"Giải mã thành công! Dữ liệu giải mã được lưu tại '{self.decrypted_csv_path}'!\n")


    
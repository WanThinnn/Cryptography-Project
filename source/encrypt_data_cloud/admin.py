import base
import sys, os, time, csv, base64, binascii
from Crypto.Random import get_random_bytes
sys.path.append(os.getcwd()) # get curent working dir and export to python paths
from mypackages import key_expansion,modes

class Admin:
    def generate_keys(self, cols):
        self.num_columns = len(cols)
        self.keys = {}
        for i in range(self.num_columns):
            self.key = get_random_bytes(16) 
            self.keys[i] = self.key
        print("Tạo key thành công!")
        return self.keys
    
    def encrypt_data(self, cols, keys_list, plaintext_csv_path, encrypted_csv_path):
        with open(plaintext_csv_path, 'r', newline='') as input_file,\
                open(encrypted_csv_path, 'w', newline='') as output_file:
            
            self.reader = csv.DictReader(input_file)
            self.fieldnames = self.reader.fieldnames  # Lấy tên cột

            writer = csv.DictWriter(output_file, fieldnames=self.fieldnames)
            writer.writeheader()
            for row in self.reader:
                for i in range(len(cols)):
                    row[cols[i]] = base.encrypt(row[cols[i]], keys_list[i])
                    # row[cols[i]] = hex_to_base64(row[cols[i]])
                # Ghi hàng đã mã hóa vào tệp CSV mới
                writer.writerow(row)
            print("Mã hoá toàn bộ dữ liệu thành công!")
            

    
    def decrypt_data(self, choices, mode_map, cols, tables, keys_list, encrypted_csv_path):
        self.name_file = input('Đặt tên file: ')
        self.decrypted_csv_path = f"dencrypted_{tables}_{self.name_file}.csv"

        # Khởi tạo từ điển để lưu trữ dữ liệu giải mã
        self.decrypted_data = {}
        for index, choice in enumerate(choices):
            self.chosen_column = mode_map.get(choice)  # Lấy giá trị tương ứng với lựa chọn của người dùng

            if self.chosen_column not in mode_map.values():
                print("Lựa chọn không hợp lệ.")
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
                        if self.chosen_column == "all_data":
                            for j, col in enumerate(cols):  # Duyệt qua mỗi cột và giải mã giá trị tương ứng
                                self.ciphertext_hex = row[col]
                                self.plaintext = base.dencrypt(self.ciphertext_hex, keys_list[j])
                                # Lưu dữ liệu giải mã vào từ điển
                                if col not in self.decrypted_data:
                                    self.decrypted_data[col] = []
                                self.decrypted_data[col].append(self.plaintext)
                        else:
                            i = cols.index(self.chosen_column)
                            self.ciphertext_hex = row[self.chosen_column]
                            self.plaintext = base.dencrypt(self.ciphertext_hex, keys_list[i])
                            # Lưu dữ liệu giải mã vào từ điển
                            if self.chosen_column not in self.decrypted_data:
                                self.decrypted_data[self.chosen_column] = []
                            self.decrypted_data[self.chosen_column].append(self.plaintext)

        except ValueError:
            print("Giải mã thất bại! Sai khoá hoặc lỗi!")  # Thông báo khi khoá không chính xác
            return

        # Lưu dữ liệu giải mã vào file CSV
        self.save_decrypted_data_to_csv()

        print(f"Giải mã thành công! Dữ liệu giải mã được lưu tại '{self.decrypted_csv_path}'.")

    def save_decrypted_data_to_csv(self):
        # Viết dữ liệu đã giải mã vào file CSV mới
        with open(self.decrypted_csv_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.decrypted_data.keys())
            writer.writeheader()

            # Sử dụng zip để kết hợp dữ liệu từ các cột thành các hàng
            for row in zip(*self.decrypted_data.values()):
                writer.writerow(dict(zip(self.decrypted_data.keys(), row)))



import base
import sys, os, time, csv, base64, binascii
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
sys.path.append(os.getcwd()) # get curent working dir and export to python paths
from mypackages import key_expansion,modes

class Admin:    
    def save_decrypted_data_to_csv(self):
        # Viết dữ liệu đã giải mã vào file CSV mới
        with open(self.decrypted_csv_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.decrypted_data.keys())
            writer.writeheader()

            # Sử dụng zip để kết hợp dữ liệu từ các cột thành các hàng
            for row in zip(*self.decrypted_data.values()):
                writer.writerow(dict(zip(self.decrypted_data.keys(), row)))
    def __init__(self):
        self.associated_data = "Đây là dữ liệu liên quan.".encode('utf-8')

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
    
    
    
    def encrypt_data(self, cols, keys_list, ivs_list, plaintext_csv_path, encrypted_csv_path):
        with open(plaintext_csv_path, 'r', newline='') as input_file,\
                open(encrypted_csv_path, 'w', newline='') as output_file:
            
            self.reader = csv.DictReader(input_file)
            self.fieldnames = self.reader.fieldnames  # Lấy tên cột

            writer = csv.DictWriter(output_file, fieldnames=self.fieldnames)
            writer.writeheader()
            for row in self.reader:
                for i in range(len(cols)):
                    row[cols[i]] = base.encrypt(row[cols[i]], keys_list[i], ivs_list[i], self.associated_data)
                # Ghi hàng đã mã hóa vào tệp CSV mới
                writer.writerow(row)
            print("Mã hoá toàn bộ dữ liệu thành công!\n")
            

    def decrypt_data(self, choices, mode_map, cols, tables, keys_list, ivs_list, encrypted_csv_path):
        self.name_file = input('Đặt tên file: ')
        self.decrypted_csv_path = f"dencrypted_{tables}_{self.name_file}.csv"

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
                                self.recovertext = base.decrypt(self.ciphertext_base64, keys_list[j], ivs_list[j], self.associated_data)
                                # Lưu dữ liệu giải mã vào từ điển
                                if col not in self.decrypted_data:
                                    self.decrypted_data[col] = []
                                self.decrypted_data[col].append(self.recovertext)
                        else:
                            i = cols.index(self.chosen_column)
                            self.ciphertext_base64 = (row[self.chosen_column])
                            self.recovertext = base.decrypt(self.ciphertext_base64, keys_list[i], ivs_list[i], self.associated_data)
                            # Lưu dữ liệu giải mã vào từ điển
                            if self.chosen_column not in self.decrypted_data:
                                self.decrypted_data[self.chosen_column] = []
                            self.decrypted_data[self.chosen_column].append(self.recovertext)

        except ValueError:
            print("Giải mã thất bại! Sai khoá hoặc lỗi!\n")  # Thông báo khi khoá không chính xác
            return

        # Lưu dữ liệu giải mã vào file CSV
        self.save_decrypted_data_to_csv()

        print(f"Giải mã thành công! Dữ liệu giải mã được lưu tại '{self.decrypted_csv_path}'!\n")


    def process(self, tables, tables_path, cols):
        while True:
            # Lựa chọn chế độ
            print("Chọn chế độ:")
            print("1. Tạo key:")
            print("2. Mã hoá:")
            print("3. Giải mã:")
            print("4. Thoát:")
            mode = int(input("Chọn: "))
            print()


            # Kiểm tra xem lựa chọn có hợp lệ không và gọi hàm tương ứng
            if mode == 1:
                num_columns = len(cols)
                self.gen_key(num_columns, tables)

                
            elif mode == 2:
                keys_list = base.read_keys_from_file(f"keys_{tables}.txt")
                ivs_list = base.read_ivs_from_file(f"ivs_{tables}.txt")
                encrypted_csv_path = f"encrypted_{tables}.csv"
                start_time = time.time()
                self.encrypt_data(cols, keys_list, ivs_list, tables_path, encrypted_csv_path)
                end_time = time.time()
                execution_time = round(end_time - start_time,2)
                print(f"Thời gian thực thi: {execution_time} giây\n")
            elif mode == 3:
                keys_list = base.read_keys_from_file(f"keys_{tables}.txt")
                ivs_list = base.read_ivs_from_file(f"ivs_{tables}.txt")
                encrypted_csv_path = f"encrypted_{tables}.csv"
                mode_map = base.create_mode_map(cols)
                base.print_cols(cols)
                # Nhập vào một chuỗi chứa các lựa chọn, mỗi lựa chọn được phân cách bằng dấu phẩy
                choice_str = input("Chọn (cách nhau 1 dấu phẩy nếu chọn nhiều hơn 1): ")
                # Tách chuỗi thành các phần tử của mảng sử dụng dấu phẩy làm dấu phân cách
                choices = choice_str.split(',')
                start_time = time.time()
                self.decrypt_data(choices, mode_map, cols, tables, keys_list, ivs_list, encrypted_csv_path)
                end_time = time.time()
                execution_time = round(end_time - start_time,2)
                print(f"Thời gian thực thi: {execution_time} giây\n")
            elif mode == 4:
                print(f"Kết thúc phiên làm việc của Admin với bảng {tables}\n")
                break

            else:
                print("Lựa chọn không hợp lệ.\n")

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
            
    def decrypt_data(self, choice, mode_map, cols, tables, keys_list, encrypted_csv_path):
        self.chosen_column = mode_map.get(choice)  # Lấy giá trị tương ứng với lựa chọn của người dùng
        self.choose = mode_map.get(choice)
        
        if  self.chosen_column not in mode_map.values():
            print("Lựa chọn không hợp lệ.")
            return
        else:
            i = int(choice) - 1  # Định nghĩa giá trị của biến i dựa trên lựa chọn của người dùng
            print("Bạn đã chọn cột:", self.chosen_column)

        self.decrypted_data = []
        
        try:
            if (i == len(cols)):
                with open(encrypted_csv_path, 'r', newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        self.decrypted_row = {}  # Tạo một hàng mới để lưu trữ các giá trị giải mã
                        for j, col in enumerate(cols):  # Duyệt qua mỗi cột và giải mã giá trị tương ứng
                            self.ciphertext_hex = row[col]
                            self.plaintext = base.dencrypt(self.ciphertext_hex, keys_list[j])
                            self.decrypted_row[col] = self.plaintext  # Thêm giá trị giải mã vào hàng mới

                        self.decrypted_data.append(self.decrypted_row)  # Thêm hàng đã giải mã vào danh sách
                    # Đường dẫn đến file CSV đã giải mã
                
                self.decrypted_csv_path = f"dencrypted_{tables}_{self.choose}.csv"

                # Viết dữ liệu đã giải mã vào file CSV mới
                with open(self.decrypted_csv_path, 'w', newline='') as csvfile:
                    self.fieldnames = self.decrypted_data[0].keys()  # Sử dụng keys của bất kỳ hàng nào để lấy tên cột
                    writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                    writer.writeheader()
                    writer.writerows(self.decrypted_data)
                print(f"Giải mã thành công! Dữ liệu giải mã '{self.choose}' được lưu tại '{self.decrypted_csv_path}'.")
                
            else:
                with open(encrypted_csv_path, 'r', newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        self.ciphertext_hex = row[self.choose]
                        self.plaintext = base.dencrypt(self.ciphertext_hex, keys_list[i])
                        row[self.choose] = self.plaintext
                        self.decrypted_data.append(row)

                # Đường dẫn đến file CSV đã giải mã
                self.decrypted_csv_path = f"dencrypted_{tables}_{self.choose}.csv"

                # Viết dữ liệu đã giải mã vào file CSV mới
                with open(self.decrypted_csv_path, 'w', newline='') as csvfile:
                    self.fieldnames = self.decrypted_data[0].keys()  # Sử dụng keys của bất kỳ hàng nào để lấy tên cột
                    writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                    writer.writeheader()
                    writer.writerows(self.decrypted_data)
                print(f"Giải mã thành công! Dữ liệu giải mã '{self.choose}' được lưu tại '{self.decrypted_csv_path}'.")
                
                
        except ValueError:
            print ("Giải mã thất bại! Sai khoá hoặc lỗi!" ) # Thông báo khi khoá không chính xác

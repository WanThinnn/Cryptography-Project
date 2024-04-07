import sys, os, time, csv, base64, binascii
import base, admin
sys.path.append(os.getcwd()) # get curent working dir and export to python paths
from mypackages import key_expansion,modes

admin_1 = admin.Admin()


switch_case = {
    1: admin_1.generate_keys,
    2: admin_1.encrypt_data,  # Đây chỉ là tên hàm, không gọi ngay lập tức
    3: admin_1.decrypt_data  # Đây cũng chỉ là tên hàm, không gọi ngay lập tức
}


tables = base.select_csv_file("database.txt")
tables_path = f"{tables}.csv"

# Lựa chọn chế độ
print("Chọn chế độ:")
print("1. Tạo key:")
print("2. Mã hoá:")
print("3. Giải mã:")
mode = int(input("Chọn: "))

# Kiểm tra xem lựa chọn có hợp lệ không và gọi hàm tương ứng
if mode == 1:
    cols = base.get_cols(tables_path)
    keys = admin_1.generate_keys(cols)
    base.save_keys_to_file(keys, f"keys_{tables}.txt")
elif mode == 2:
    cols = base.get_cols(tables_path)
    keys_list = base.read_keys_from_file(f"keys_{tables}.txt")
    encrypted_csv_path = f"encrypted_{tables}.csv"
    start_time = time.time()
    admin_1.encrypt_data(cols, keys_list, tables_path, encrypted_csv_path)
    end_time = time.time()
    execution_time = round(end_time - start_time,2)
    print(f"Thời gian thực thi: {execution_time} giây")
    
elif mode == 3:
    keys_list = base.read_keys_from_file(f"keys_{tables}.txt")
    encrypted_csv_path = f"encrypted_{tables}.csv"
    cols = base.get_cols(tables_path)
    mode_map = base.create_mode_map(cols)
    base.print_cols(cols)
    choice = input("Enter choice: ")
    start_time = time.time()
    admin_1.decrypt_data(choice, mode_map, cols, tables, keys_list, encrypted_csv_path)
    end_time = time.time()
    execution_time = round(end_time - start_time,2)
    print(f"Thời gian thực thi: {execution_time} giây")
else:
    print("Lựa chọn không hợp lệ.")

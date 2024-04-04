import csv

def get_cols(csv_file_path):
    cols = []
    # Đọc dòng đầu tiên của file CSV và lưu vào mảng cols
    with open(csv_file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        cols = next(reader)  # Đọc dòng đầu tiên và lưu vào mảng cols
    return cols


def print_cols(cols):
    print('Moi nhap cot can giai ma: ')
    # In ra tên các cột
    for i, col in enumerate(cols, start=1):
        print(f"{i}. {col}")

def get_tables(file_path):
    result = []  # Khởi tạo một list để lưu trữ các hàng từ file CSV
    with open(file_path, 'r') as file:
        # Đọc từng dòng của file văn bản
        for line in file:
            # Xử lý dòng là một bảng CSV
                result.append(line.strip())  # Thêm dòng sau khi loại bỏ dấu xuống dòng vào mảng
    return result


def print_tables(tables):
    print('Moi nhap bang can giai ma: ')
    for i, table in enumerate(tables, start=1):
        print(f"{i}. {table}")


tbls = get_tables("database.txt")
print_tables(tbls)
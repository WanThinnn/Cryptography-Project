import sys, os, time, csv, base64, binascii
import base, admin, user
sys.path.append(os.getcwd()) # get curent working dir and export to python paths
from mypackages import key_expansion,modes



# Sử dụng hàm login
user_type = base.login()

if user_type == "admin":
    admin_1 = admin.Admin()
    tables, tables_path = base.process_database()
    admin_1.process(tables, tables_path)

elif user_type == "user":
    user_1 = user.User()
    tables, tables_path = base.process_database()
    user_1.process(tables, tables_path)

else:
    print("Lỗi, đăng nhập thất bại!")








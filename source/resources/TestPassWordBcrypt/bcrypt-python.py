import bcrypt
import mysql.connector.errors
from loginDbMySQL import insert, getUserPWHash




class LoginSystem:
    @staticmethod
    def promptForCreds():
        username = input("Nhập tên người dùng: ")
        password = input("Nhập mật khẩu: ")
        return username, password

    @staticmethod
    def passwordHashing(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14)).decode('utf-8')

    @staticmethod
    def validateCredentials(password, password_hash):
        return bcrypt.checkpw(password.encode('utf8'), password_hash.encode('utf8'))

    def sign_up(self):
        username, password = self.promptForCreds()
        insert(username, self.passwordHashing(password))

    def login(self):
        username, password = self.promptForCreds()
        password_hash = getUserPWHash(username)
        if password_hash:
            return self.validateCredentials(password, password_hash)
        return False

def main():
    login_instance = LoginSystem()

    while True:
        value = input("1-Đăng nhập, 2-Đăng ký, 3-Thoát\n")
        if value == "1":
            if login_instance.login():
                print("Chào mừng!")
            else:
                print("Truy cập bị từ chối")
        elif value == "2":
            try:
                login_instance.sign_up()
                print("Đăng ký thành công.")
            except mysql.connector.errors.IntegrityError:
                print("Không thể đăng ký - tên người dùng đã tồn tại.")
            except Exception as e:
                print(f"Đã xảy ra lỗi: {e}")
        elif value == "3":
            break  # thoát
        else:
            continue

if __name__ == "__main__":
    main()

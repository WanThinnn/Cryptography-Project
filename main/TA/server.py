from CPABE import CPABE
from f_cpabe import setup, gen_secret_key, encrypt_message, decrypt_message
import socket
import ssl
import sys
import os

class Server:
    def __init__(self, host='192.168.1.4', port=10023, certfile=None, keyfile=None):
        self.host = host
        self.port = port
        self.certfile = certfile
        self.keyfile = keyfile
        self.is_running = True
        self.cpabe = CPABE("AC17")
        # self.setup_key("setup/")  # Automatically run setup_key during initialization

    def TAsetup(self, path):
        try:
            setup(self.cpabe, path)
            print('Setup successfully completed.')
        except Exception as e:
            print(f"Error during setup: {e}")

    def TAgenkey(self, conn, addr, msg, public_key_file, master_key_file, private_key_file_path):
        try:
            mode, attributes = msg.split('|', 1)  # Chỉ tách lần đầu tiên tìm thấy '|'
            print(f"Mode: {mode}, Attributes: {attributes}")

            if mode == 'genkey':
                # Tạo khóa bí mật
                gen_secret_key(self.cpabe, public_key_file, master_key_file, attributes, private_key_file_path)
                
                # Đọc nội dung của file khóa bí mật
                with open(private_key_file_path, 'rb') as private_key_file:
                    private_key = private_key_file.read()
                    conn.sendall(private_key + b'END_OF_FILE')  # Gửi khóa bí mật đến client

                print('Generated secret key for client:', addr)
        except Exception as e:
            print(f"Error generating secret key for {addr}: {e}")
        finally:
            # Xóa file khóa bí mật sau khi đã gửi
            if os.path.exists(private_key_file_path):
                os.remove(private_key_file_path)
            conn.close()
                
    def TASendPubKey(self, conn, addr, public_key_file):
        try:
            # Đọc nội dung của file khóa công khai
            with open(public_key_file, 'rb') as public_key_file:
                public_key = public_key_file.read()
                conn.sendall(public_key + b'END_OF_FILE')  # Gửi khóa công khai đến client

            print('Send public key for client:', addr)
        except Exception as e:
            print(f"Error sending public key to {addr}: {e}")
        finally:
            conn.close()

    def handle_request(self, conn, msg, addr):
        try:
            if msg == 'setup':
                self.TAsetup("setup/")
            elif msg.startswith('genkey|'):
                self.TAgenkey(conn, addr, msg, "setup/public_key.bin", "setup/master_key.bin", "setup/private_key.bin")
            elif msg == 'get_pub_key':
                self.TASendPubKey(conn, addr, "setup/public_key.bin")
            else:
                conn.sendall('Invalid choice'.encode('utf-8'))
                print(f"Invalid choice from {addr}")
        except Exception as e:
            print(f"Error handling request from {addr}: {e}")
        finally:
            conn.close()

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=self.certfile, keyfile=self.keyfile)

        while self.is_running:
            try:
                conn, addr = server_socket.accept()
                conn = context.wrap_socket(conn, server_side=True)
                msg = conn.recv(1024).decode()
                self.handle_request(conn, msg, addr)
            except Exception as e:
                print(f"Error accepting connection: {e}")
                if conn:
                    conn.close()

        server_socket.close()
    
    def setup_key(self, path):
        self.TAsetup(path)

if __name__ == "__main__":
    server = Server(certfile='ecc_cert.pem', keyfile='private_key.pem')
    server.start()

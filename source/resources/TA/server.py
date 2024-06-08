from CPABE import CPABE
from f_cpabe import setup, gen_secret_key, encrypt_message, decrypt_message
import socket
import ssl
import sys
import os

class Server:
    def __init__(self, host='192.168.1.5', port=10023, certfile=None, keyfile=None):
        self.host = host
        self.port = port
        self.certfile = certfile
        self.keyfile = keyfile
        self.is_running = True
        self.cpabe = CPABE("AC17")

    def TAsetup(self, conn, msg, addr, path):
        if msg == 'setup':
            setup(self.cpabe, path)
            public_key_file = path + 'public_key.bin'
            with open(public_key_file, 'rb') as public_key_file:
                public_key = public_key_file.read()
                conn.sendall(public_key)
            print('Setup sucessfully for:', addr)
            conn.close()

    def TAgenkey(self, conn, msg, addr, public_key_file, master_key_file, attributes, private_key_file):
        if msg == 'genkey':
            gen_secret_key(self.cpabe, public_key_file, master_key_file, attributes, private_key_file)
            with open(private_key_file, 'rb') as private_key_file:
                private_key = private_key_file.read()
                conn.sendall(private_key)
            print('Generated secret key for client:', addr)
            conn.close()

    def TAencrypt(self, conn, msg, addr, public_key_file, plaintext_file, ciphertext_file):
        if msg == 'encrypt':
            encrypt_message(self.cpabe, public_key_file, plaintext_file, ciphertext_file)
            with open(ciphertext_file, 'rb') as ciphertext:
                data = ciphertext.read()
                conn.sendall(data)
            print('Encrypted data sent to client:', addr)
            conn.close()

    def TAdecrypt(self, conn, msg, addr, public_key_file, private_key_file, cipher_text_file, recover_text_file):
        if msg == 'decrypt':
            self.receive_private_key(conn, "setup/private_key.bin")
            decrypt_message(self.cpabe, public_key_file, 'setup/private_key.bin', cipher_text_file, recover_text_file)
            with open(recover_text_file, 'rb') as recovered_text:
                data = recovered_text.read()
                conn.sendall(data)
                # Gửi END_OF_FILE để đánh dấu kết thúc quá trình truyền dữ liệu
                conn.sendall(b'END_OF_FILE')
            print('Decrypted data sent to client:', addr)
            conn.close()
            
    def receive_private_key(self, conn, private_key_file):
        with open(private_key_file, 'wb') as f:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                if data.endswith(b'END_OF_FILE'):
                    f.write(data[:-len(b'END_OF_FILE')])
                    break
                f.write(data)
        print("Private key received successfully.")


    
    def handle_request(self, conn, msg, addr, private_key=None):
        if msg == 'setup':
            self.TAsetup(conn, msg, addr, "setup/")
        elif msg == 'genkey':
            self.TAgenkey(conn, msg, addr, "setup/public_key.bin", "setup/master_key.bin", "A,B", "setup/private_key.bin")
        elif msg == 'encrypt':
            self.TAencrypt(conn, msg, addr, "setup/public_key.bin", "key.csv", "encrypted_data.csv")
        elif msg == 'decrypt':
            
            self.TAdecrypt(conn, msg, addr, "setup/public_key.bin", "setup/private_key.bin", "encrypted_data.csv", "decrypted_data.csv")
        else:
            conn.sendall('Invalid choice'.encode('utf-8'))
            print(f"Invalid choice from {addr}")
            conn.close()

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=self.certfile, keyfile=self.keyfile)

        while self.is_running:
            conn, addr = server_socket.accept()
            conn = context.wrap_socket(conn, server_side=True)
            msg = conn.recv(1024).decode()
            self.handle_request(conn, msg, addr)

        server_socket.close()

if __name__ == "__main__":
    server = Server(certfile='ecc_cert.pem', keyfile='private_key.pem')
    server.start()

import socket
import ssl
import os
import random
import string

class Server:
    def __init__(self, host='192.168.50.1', port=10023, certfile=None, keyfile=None):
        self.host = host
        self.port = port
        self.certfile = certfile
        self.keyfile = keyfile
        self.is_running = True

    def handle_request(self, conn, msg, addr):
        if msg == '1':
            result = self.perform_calculation()
            conn.sendall(result.encode('utf-8'))
            print('Sent result of calculation to client', addr)
            conn.close()
            
        elif msg == '2':
            result = self.perform_multiplication()
            conn.sendall(result.encode('utf-8'))
            print('Sent result of multiplication to client', addr)
            conn.close()
            
        elif msg == '3':
            result = self.generate_random_string()
            conn.sendall(result.encode('utf-8'))
            print('Sent random string to client', addr)
            conn.close()
            
        elif msg == '4':
            conn.sendall('Exiting...'.encode('utf-8'))
            print('Client disconnect!', addr)
            conn.close()

            
        elif msg == '5':
            self.send_random_file(conn)
        
        else:
            conn.sendall('Invalid choice'.encode('utf-8'))
            print('Invalid choice')
            conn.close()

    def perform_calculation(self):
        num1 = 10
        num2 = 5
        result = num1 + num2
        return str(result)

    def perform_multiplication(self):
        num1 = 10
        num2 = 5
        result = num1 * num2
        return str(result)

    def generate_random_string(self):
        return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=32))

    def send_random_file(self, conn):
        random_data = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        file_path = os.path.abspath('random_data.txt')
        with open(file_path, 'w') as f:
            f.write(random_data)
        with open(file_path, 'rb') as f:
            data = f.read(1024)
            while data:
                conn.send(data)
                data = f.read(1024)
        conn.sendall(b'END_OF_FILE')
        os.remove('random_data.txt')
        print('Sent random data file to client')
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

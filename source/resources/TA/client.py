import socket
import ssl
import sys
import os

class Client:
    def __init__(self, host='192.168.1.3', port=10023):
        self.host = host
        self.port = port

    def connect_to_server(self, mode, private_key=None, save_path=None, file_name=None):
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.load_verify_locations("ecc_cert.pem")
        context.check_hostname = False
        print("Connected to the server")
        try:
            conn = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=self.host)
            conn.connect((self.host, self.port))
            if conn.cipher():
                print("Connection is encrypted with:", conn.cipher()[0])
            else:
                print("Connection is not encrypted.")

            if mode == 'setup' or mode == 'genkey':
                if save_path is None or file_name is None:
                    print("Please provide save path and file name.")
                    conn.close()
                    return  # Thoát vòng lặp khi thiếu thông tin

                conn.sendall(mode.encode('utf-8'))
                with open(os.path.join(save_path, file_name), 'wb') as f:
                    data = conn.recv(1024)
                    while data:
                        if data.endswith(b'END_OF_FILE'):
                            f.write(data[:-len(b'END_OF_FILE')])
                            break
                        f.write(data)
                        data = conn.recv(1024)
                print("File received successfully.")
                conn.close()
                return  
            

        except Exception as e:
            print("Error:", e)
            conn.close()
            return  # Thoát vòng lặp nếu có lỗi xảy ra

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 client.py <server_ip> <server_port> [setup|genkey|encrypt|decrypt]")
        sys.exit(1)
        
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    mode = sys.argv[3]
    if mode == 'setup':
        if len(sys.argv) != 6:
            print("Usage: python3 client.py <server_ip> <server_port> setup <path_to_save> <file_name>")
            sys.exit(1)
        client = Client(host=server_ip, port=server_port)
        client.connect_to_server(sys.argv[3], None, sys.argv[4], sys.argv[5])
    elif mode == 'genkey':
        if len(sys.argv) != 6:
            print("Usage: python3 client.py <server_ip> <server_port> genkey <path_to_save> <file_name>")
            sys.exit(1)
        client = Client(host=server_ip, port=server_port)
        client.connect_to_server(sys.argv[3], None, sys.argv[4], sys.argv[5])

import socket
import ssl
import sys
import os

class Client:
    def __init__(self, host='192.168.50.1', port=10023):
        self.host = host
        self.port = port

    def connect_to_server(self, choice, save_path=None, file_name=None):
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
                
            if choice in ('1', '2', '3', '4'):
                conn.sendall(choice.encode('utf-8'))
                response = b''
                data = conn.recv(1024)
                response += data
                print("Server response:", response.decode('utf-8'))

                if choice == '4':
                    conn.close()


            elif choice == '5':
                if save_path is None or file_name is None:
                    print("Please provide save path and file name.")
                    conn.close()
                    return  # Thoát vòng lặp khi thiếu thông tin

                conn.sendall(choice.encode('utf-8'))
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
                return  # Thoát vòng lặp khi choice là '5'

            else:
                print("Invalid choice")
                conn.close()
                return  # Thoát vòng lặp khi choice không hợp lệ

        except Exception as e:
            print("Error:", e)
            conn.close()
            return  # Thoát vòng lặp nếu có lỗi xảy ra

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 client.py <server_ip> <server_port> <choice> [<save_path> <file_name>]")
        sys.exit(1)
        
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    
    if sys.argv[3] == '5':
        if len(sys.argv) != 6:
            print("Usage: python3 client.py <server_ip> <server_port> <choice> <save_path> <file_name>")
            sys.exit(1)
        client = Client(host=server_ip, port=server_port)
        client.connect_to_server(sys.argv[3], sys.argv[4], sys.argv[5])
    elif sys.argv[3] != '5':
        if len(sys.argv) != 4:
            print("Usage: python3 client.py <server_ip> <server_port> <choice> ")
            sys.exit(1)
        client = Client(host=server_ip, port=server_port)
        client.connect_to_server(sys.argv[3], save_path=None, file_name=None)
    

   



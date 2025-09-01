# server2.py
import socket
import os

HOST = '127.0.0.1'
PORT = 65433  # Port for SERVER2

def handle_request(conn):
    try:
        data = conn.recv(1024).decode()
        print(f"SERVER 2: Received request for file '{data}'")

        file_path = os.path.join('server2_files', data)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
            conn.sendall(content.encode())
            print(f"SERVER 2: Sent content of '{data}'")
        else:
            conn.sendall(b'FILE_NOT_FOUND')
            print(f"SERVER 2: File '{data}' not found. Sent 'FILE_NOT_FOUND' message.")
    except Exception as e:
        print(f"SERVER 2: Error handling request: {e}")
    finally:
        conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"SERVER 2 listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            print(f"SERVER 2: Connected by {addr}")
            handle_request(conn)

if __name__ == '__main__':
    main()
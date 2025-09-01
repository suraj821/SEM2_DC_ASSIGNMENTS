# server1.py
import socket
import os
import hashlib

HOST = '0.0.0.0' # For listening to the client
SERVER1_PORT = 65432

# !!! CRITICAL: Replace '172.31.25.178' with the actual Private IP of your SERVER2 EC2 instance
SERVER2_HOST = '172.31.21.83'
SERVER2_PORT = 65433

def get_file_hash(filepath):
    """Calculates the SHA256 hash of a file."""
    if not os.path.exists(filepath):
        return None
    
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def request_file_from_server2(filename):
    """Sends a request to SERVER2 and returns its response."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            # Connect to SERVER2 using its private IP address
            s.connect((SERVER2_HOST, SERVER2_PORT))
            s.sendall(filename.encode())
            response = s.recv(4096).decode()
            return response
        except ConnectionRefusedError:
            print("SERVER 1: Could not connect to SERVER 2. Check its status.")
            return 'CONNECTION_ERROR'
        except Exception as e:
            print(f"SERVER 1: An error occurred communicating with SERVER 2: {e}")
            return 'COMMUNICATION_ERROR'

def handle_client_request(conn):
    try:
        filename = conn.recv(1024).decode()
        print(f"\nSERVER 1: Received client request for file '{filename}'")

        # Get file from SERVER 1's local directory
        s1_file_path = os.path.join('server1_files', filename)
        s1_content = None
        if os.path.exists(s1_file_path):
            with open(s1_file_path, 'r') as f:
                s1_content = f.read()
        
        # Get file from SERVER 2
        s2_content = request_file_from_server2(filename)

        response_to_client = ''
        
        # Scenario 1: File not found on either server
        if s1_content is None and s2_content == 'FILE_NOT_FOUND':
            response_to_client = 'FILE_NOT_FOUND'
            print(f"SERVER 1: File '{filename}' not found on either server. Sending 'FILE_NOT_FOUND'.")

        # Scenario 2: File found on one server but not the other
        elif s1_content is None: # Found only on SERVER 2
            response_to_client = f'Found on SERVER 2 only:\n{s2_content}'
            print(f"SERVER 1: File '{filename}' found on SERVER 2 only.")
        elif s2_content == 'FILE_NOT_FOUND': # Found only on SERVER 1
            response_to_client = f'Found on SERVER 1 only:\n{s1_content}'
            print(f"SERVER 1: File '{filename}' found on SERVER 1 only.")

        # Scenario 3: File found on both servers, compare content
        else:
            if s1_content == s2_content:
                response_to_client = f'Both files are identical.\nContent:\n{s1_content}'
                print(f"SERVER 1: Files are identical. Sending one copy.")
            else:
                response_to_client = f'Files are different.\n\nContent from SERVER 1:\n{s1_content}\n\nContent from SERVER 2:\n{s2_content}'
                print(f"SERVER 1: Files are different. Sending both versions.")

        conn.sendall(response_to_client.encode())
        print("SERVER 1: Sent response to client.")

    except Exception as e:
        print(f"SERVER 1: Error handling client request: {e}")
    finally:
        conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, SERVER1_PORT))
        s.listen()
        print(f"SERVER 1 listening on {HOST}:{SERVER1_PORT}")
        while True:
            conn, addr = s.accept()
            print(f"SERVER 1: Connected by {addr}")
            handle_client_request(conn)

if __name__ == '__main__':
    main()
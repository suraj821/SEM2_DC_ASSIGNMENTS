# client.py
import socket

HOST = '127.0.0.1'
PORT = 65432  # Connects to SERVER 1

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print("Client connected to SERVER 1.")
            
            while True:
                filename = input("Enter filename to request (or 'exit' to quit): ")
                if filename.lower() == 'exit':
                    break
                
                s.sendall(filename.encode())
                print(f"Client: Sent request for '{filename}'")
                
                response = s.recv(4096).decode()
                print("\n--- SERVER RESPONSE ---")
                print(response)
                print("-----------------------\n")
                
        except ConnectionRefusedError:
            print("Client: Could not connect to SERVER 1. Make sure it's running.")
        except Exception as e:
            print(f"Client: An error occurred: {e}")

if __name__ == '__main__':
    main()
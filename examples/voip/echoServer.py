import socket

host = "0.0.0.0"
port = 8080
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
print(f"Server listening on {host}:{port}")
server_socket.listen()

try:
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            client_socket.sendall(data)
        client_socket.close()
        print(f"Connection closed with {client_address}")
except KeyboardInterrupt:
    print("\nServer shutting down...")
finally:
    server_socket.close()

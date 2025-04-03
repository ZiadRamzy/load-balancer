import socket

def start_backend_server(port: int) -> None:
    """
    Starts a backend server that listens for incoming client connections on the specified port.
    When a client connects, it sends a simple HTTP response with a 'Hello From Backend Server' message.

    Args:
        port: The port on which the backend server will listen for incoming connections.

    Returns:
        None: This function runs an infinite loop accepting client requests and responding with a fixed message.
    """

    server_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(5)
    print(f"Backend server started on port {port}")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Received request from {address}")

        response: str = 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello From Backend Server'
        client_socket.sendall(response.encode())
        client_socket.close()


if __name__ == "__main__":
    start_backend_server(8001) 


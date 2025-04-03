import socket
import threading
from typing import Optional

BACKEND_SERVERS = ['localhost:8001', 'localhost:8002']

def forward_request(client_socket: socket.socket, backend: str) -> None:
    """
    Forwards the HTTP request from the client to a specified backend server,
    receives the response, and sends it back to the client.

    Args:
        client_socket: The socket object representing the client connection.
        backend: The backend server address to forward the request to.

    Returns:
        None: The function sends the response back to the client and closes the client connection.
    """
    
    try:
        backend_host, backend_port = backend.split(':')
        backend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        backend_socket.connect((backend_host, int(backend_port)))

        request = client_socket.recv(1024)

        backend_socket.sendall(request)

        response = backend_socket.recv(1024)

        client_socket.send(response)

        backend_socket.close()
    except Exception as error:
        print(f"Error while forwarding the request: {error}")
    finally:
        client_socket.close()


def handle_client(client_socket: socket.socket) -> None:
    """
    Handles an incoming client request and forwards it to one of the backend servers.

    Args:
        client_socket: The socket object representing the client connection.

    Returns:
        None: The function spawns a thread to handle the client request and forward it to a backend server.
    """

    backend: str = BACKEND_SERVERS[0]
    forward_request(client_socket, backend)


def start_load_balancer(host: str, port: int) -> None:
    """
    Starts the load balancer that listens for incoming client connections and
    delegates the requests to the backend servers.

    Args:
        host: The host address where the load balancer will listen.
        port: The port number where the load balancer will listen.

    Returns:
        None: The function runs an infinite loop accepting client requests.
    """

    server_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Load Balancer started on {host}:{port}")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Received request from {address}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    start_load_balancer('localhost', 80)
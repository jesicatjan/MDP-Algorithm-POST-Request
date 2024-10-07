import socket

def run_client(server_ip, server_port=8000):
    """
    Function to run a client that connects to the server and sends a "hello" message.
    
    Args:
        server_ip (str): The IP address of the server to connect to.
        server_port (int): The port number of the server to connect to. Default is 8000.
    """
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to the server using its IP address and port
        client_socket.connect((server_ip, server_port))
        print(f'Connected to server at {server_ip}:{server_port}')
        
        # Send a "hello" message
        client_socket.sendall(b"hello")
        print('Sent "hello" message to the server.')

        # Receive the response from the server
        data = client_socket.recv(1024)  # Receive up to 1024 bytes
        print(f'Received message from server: {data.decode()}')

    finally:
        # Close the connection
        client_socket.close()
        print("Connection closed.")

# To run the client, just call this function with the server's IP address
if __name__ == "__main__":
    # Replace 'your_server_ip' with the actual IP address of the server laptop
    # server_ip = 'your_server_ip'  # Example: '192.168.1.100'
    
    server_ip = '10.91.228.108'

    run_client(server_ip)

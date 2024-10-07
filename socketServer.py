import socket

def run_server(host='0.0.0.0', port=8080):
    """
    Function to run a simple server that listens for a connection and
    expects to receive a "hello" message from a client.
    
    Args:
        host (str): The hostname or IP address to bind the server to. Default is '0.0.0.0'.
        port (int): The port number to bind the server to. Default is 8000.
    """
    # Set up the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))  # Bind to the specified host and port
    server_socket.listen(1)  # Listen for incoming connections (backlog of 1)

    print(f'Server listening on {host}:{port}...')
    
    try:
        # Accept a connection
        conn, addr = server_socket.accept()
        print(f'Connected by {addr}')
        
        # Receive the message (in this case, expecting "hello")
        data = conn.recv(1024)  # Receive up to 1024 bytes (for small text messages)
        
        if not data:
            print("No data received. Closing connection.")
        else:
            # Decode the message and strip any extra spaces
            message = data.decode().strip()
            print(f"Received message: {message}")

            # Check if the message is "hello"
            if message.lower() == "hello":
                print("Hello message received successfully!")
            else:
                print(f"Unexpected message: {message}")

    finally:
        # Close the connection explicitly
        conn.close()
        print("Connection closed.")
        
        # Close the server socket
        server_socket.close()
        print("Server socket closed. Exiting now.")

# To run the server, just call this function
if __name__ == "__main__":
    run_server()  # This will run the server on '0.0.0.0' and port 8000

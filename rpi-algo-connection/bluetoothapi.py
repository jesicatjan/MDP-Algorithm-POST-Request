import bluetooth
from format import formatToAlgo, formatToSTM
from sendRequest import sendRequest

class BluetoothAPI:
    # Static variables: MAC addresses, port, and buffer size
    MAC_ADDRESS = 'AA:AA:AA:AA:AA:AA'  # Raspberry Pi's MAC address
    TABLET_BLUETOOTH = '90:EE:C7:E7:D6:40'  # Tablet Bluetooth MAC address
    PORT_NUMBER = 1
    READ_BUFFER_SIZE = 5096

    def __init__(self):
        self.server_socket = None
        self.client_socket = None

    def connect(self):
        try:
            # Set up the Bluetooth server socket
            self.server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.server_socket.bind((self.MAC_ADDRESS, self.PORT_NUMBER))
            self.server_socket.listen(1)
            print(f"[BT] Listening on {self.MAC_ADDRESS}:{self.PORT_NUMBER}...")

            # Accept a connection from the tablet
            print(f"[BT] Waiting for connection from {self.TABLET_BLUETOOTH}...")
            self.client_socket, client_info = self.server_socket.accept()
            if client_info[0] == self.TABLET_BLUETOOTH:
                print(f"[BT] Connected to {client_info}")
            else:
                print(f"[BT] Connected to an unknown device: {client_info}")
                self.disconnect()
        except Exception as e:
            print(f"[BT] Failed to start Bluetooth server: {e}")

    def read(self):
        try:
            if self.client_socket:
                data = self.client_socket.recv(self.READ_BUFFER_SIZE)
                if data:
                    print(f"[BT] Received: {data.decode('utf-8')}")
                    return data.decode('utf-8')
            else:
                print("[BT] No client is connected.")
        except OSError:
            print("[BT] Connection closed.")
        except Exception as e:
            print(f"[BT] Error reading data: {e}")
        return None

    def write(self, message):
        try:
            if self.client_socket:
                self.client_socket.send(message.encode('utf-8'))
                print(f"[BT] Sent: {message}")
            else:
                print("[BT] No client is connected.")
        except Exception as e:
            print(f"[BT] Error sending data: {e}")

    def disconnect(self):
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None
        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None
        print("[BT] Disconnected from client.")

# Example usage
if __name__ == "__main__":
    bt_api = BluetoothAPI()
    bt_api.connect()

    waiting_for_initial_positions = False
    initialPositions = None

    while True:
        message = bt_api.read()
        if message:
            print(f"Processing message: {message}")

            # Get the message after "CALL ALGO", which is the position information
            if waiting_for_initial_positions:
                initialPositions = message
                print(f"Stored initialPositions: {initialPositions}")

                # Call formatToAlgo
                formatted_algo = formatToAlgo(initialPositions)
                print(f"Stored formatted_algo: {formatted_algo}")

                # Send the formatted message to the algorithm
                response = sendRequest(formatted_algo)

                # Call formatToSTM
                formatted_stm = formatToSTM(response)

                # Reset the flag
                waiting_for_initial_positions = False
            
            # Check if the message is "CALL ALGO"
            elif message == "CALL ALGO":
                waiting_for_initial_positions = True
            
            bt_api.write(f"Received: {message}")
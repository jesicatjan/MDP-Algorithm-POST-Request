import bluetooth
import serial
import time
import formatToAlgo
import formatToSTM
import sendRequest

# Bluetooth API class to manage the Bluetooth connection
class BluetoothAPI:
    MAC_ADDRESS = 'E4:5F:01:55:A6:F3'  # Raspberry Pi's MAC address
    TABLET_BLUETOOTH = '48:61:EE:2A:A9:52'  # Android tablet Bluetooth MAC address
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

            # Accept a connection from the Android device
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
                # Receive data from the Android device
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
                # Send a message back to the Android device
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

# Serial API class to manage serial communication with the STM board
class SerialAPI:
    SERIAL_PORT = '/dev/ttyUSB0'  # Change this if the STM board is connected on another port
    BAUD_RATE = 115200

    def __init__(self):
        self.serial_connection = None

    def connect(self):
        while self.serial_connection is None:
            try:
                # Connect to the STM board via serial
                self.serial_connection = serial.Serial(self.SERIAL_PORT, self.BAUD_RATE, timeout=1)
                print(f"[STM] Connected to STM on {self.SERIAL_PORT} at {self.BAUD_RATE} baud.")
            except serial.SerialException as e:
                print(f"[STM] Failed to connect: {e}")
                time.sleep(1)

    def write(self, message):
        print(f"[STM] Sending message to STM: {message}")
        try:
            # Send the message to the STM board via serial
            self.serial_connection.write(message.encode('utf-8'))
            print("[STM] Message sent successfully.")
        except Exception as e:
            print(f"[STM] Failed to send: {e}")

    def read(self):
        try:
            # Read data from the STM board via serial
            data = self.serial_connection.read_until(b'A').decode('utf-8')
            print(f"[STM] Received: {data}")
            return data
        except Exception as e:
            print(f"[STM] Failed to read: {e}")
        return None

    def disconnect(self):
        if self.serial_connection:
            self.serial_connection.close()
            print("[STM] Serial connection closed.")
            self.serial_connection = None

# Main program to integrate both Bluetooth and STM communication
def main():
    # Step 1: Connect to STM board via serial
    stm_api = SerialAPI()
    stm_api.connect()

    # Step 2: Connect to Android device via Bluetooth
    bt_api = BluetoothAPI()
    bt_api.connect()

    waiting_for_initial_positions = False
    initialPositions = None
    
    # Step 3: Relay messages from Bluetooth to STM and vice versa
    while True:

        # Add a delay to prevent the loop from running too fast
        time.sleep(1)

        # Read data from the Android device
        bt_message = bt_api.read()

        if waiting_for_initial_positions:
            initialPositions = bt_message
            print(f"Stored initialPositions: {initialPositions}")

            # Format and POST request to the algorithm server
            formatted_algo = formatToAlgo(initialPositions)
            response = sendRequest(formatted_algo)
            formatted_stm = formatToSTM(response)

            # Send the commands to STM
            stm_api.write(formatted_stm)
            stm_response = stm_api.read()

            if stm_response:
                # Send the STM response back to the Android device
                bt_api.write(f"STM responded: {stm_response}")
                print(f"[Main] Relayed response back to Android: {stm_response}")
            
            # Reset the flag
            waiting_for_initial_positions = False
            continue
        
        # Check if the message is "BEGIN"
        elif bt_message == "BEGIN":
            waiting_for_initial_positions = True
            continue
    
        elif bt_message:
            print(f"[Main] Received from Android: {bt_message}")

            # Send the received message to the STM board
            stm_api.write(bt_message)

            # Read response from the STM board
            stm_response = stm_api.read()
            if stm_response:
                # Send the STM response back to the Android device
                bt_api.write(f"STM responded: {stm_response}")
                print(f"[Main] Relayed response back to Android: {stm_response}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[Main] Program terminated by user.")

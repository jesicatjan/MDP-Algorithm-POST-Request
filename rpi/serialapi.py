import serial
import time

class SerialAPI:
    # Static variables: serial port and baud rate for the STM board
    SERIAL_PORT = '/dev/ttyUSB0'
    BAUD_RATE = 115200

    def __init__(self):
        self.serial_connection = None

    def connect(self):
        while self.serial_connection is None:
            try:
                self.serial_connection = serial.Serial(self.SERIAL_PORT, self.BAUD_RATE, timeout=1)
                print(f"[STM] Connected to STM on {self.SERIAL_PORT} at {self.BAUD_RATE} baud.")
            except serial.SerialException as e:
                print(f"[STM] Failed to connect: {e}")
                time.sleep(1)

    def write(self, message):
        print(f"[STM] Sending message to STM: {message}")
        try:
            self.serial_connection.write(message.encode('utf-8'))
            print("[STM] Message sent successfully.")
        except Exception as e:
            print(f"[STM] Failed to send: {e}")

    def read(self):
        try:
            data = self.serial_connection.read_until(b'A').decode('utf-8')
            print(f"[STM] Received: {data}")
            return data
        except Exception as e:
            print(f"[STM] Failed to read: {e}")
        return None

    def check_connection(self):
        return self.serial_connection and self.serial_connection.is_open

    def disconnect(self):
        if self.serial_connection:
            self.serial_connection.close()
            print("[STM] Serial connection closed.")
            self.serial_connection = None

# Example usage
if __name__ == "__main__":
    stm_api = SerialAPI()
    stm_api.connect()

    while True:
        message = stm_api.read()
        if message:
            print(f"Processing message: {message}")
            stm_api.write(f"Echo: {message}")

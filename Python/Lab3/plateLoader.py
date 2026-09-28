import serial
import time


class PlateLoader:
    def __init__(self, port="/dev/ttyACM0"):
        self.port = port
        self.ser = None

    def connect(self):
        if self.ser and self.ser.is_open:
            return
        self.ser = serial.Serial(port=self.port, baudrate=19200, timeout=5)
        time.sleep(2.0)
        self.ser.reset_input_buffer()

    def disconnect(self):
        if self.ser and self.ser.is_open:
            self.ser.close()

    def send_command(self, command):
        self.ser.reset_input_buffer()
        message_bytes = (command + "\n").encode()
        print(message_bytes)

        self.ser.write(message_bytes)

        response_bytes = self.ser.readline()
        print(response_bytes)
        response = response_bytes.decode().strip()
        return response


if __name__ == "__main__":
    print("Quick PlateLoader testing")
    loader = PlateLoader()
    loader.connect()
    response = loader.send_command("RESET")
    print("Response: ", response)
    loader.disconnect()
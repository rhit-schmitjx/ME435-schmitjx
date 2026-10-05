import serial
import time

print("Learning Pyserial")

# ser = serial.Serial(port="/dev/cu.usbmodem21201", baudrate=19200, timeout=10)
ser = serial.Serial(port="/dev/ttyUSB0", baudrate=19200, timeout=10)

time.sleep(2.0)

ser.reset_input_buffer()
message = "RESET"
print(message)
message_bytes = (message + "\n").encode()
print(message_bytes)

ser.write(message_bytes)

response_bytes = ser.readline()
print(response_bytes)
response = response_bytes.decode().strip()
print(response)

ser.close()
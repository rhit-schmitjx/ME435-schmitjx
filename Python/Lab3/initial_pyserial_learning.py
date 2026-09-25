import time
import serial

print("Learning Pyserial")

ser = serial.Serial('COM9', '19200', timeout=10)

time.sleep(2.0) # necessary sometimes

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
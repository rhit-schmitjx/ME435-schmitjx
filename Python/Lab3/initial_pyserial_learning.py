import serial

print("Learning Pyserial")

ser = serial.Serial('COM9', '19200', timeout=10)

while not ser.is_open:
    print("Opening...")

# TODO: Use the ser object

ser.close()
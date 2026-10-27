import gpiozero as gz
import time
class Ultrasonic:
    def __init__(self):
        self.sensor = gz.DistanceSensor(echo=22, trigger=27)

    def get_cm(self):
        return self.sensor.distance * 100

class LineSensors:
    def __init__(self, port):
        self.port = port
        # Initialize the line sensors on the given port

    def get_left(self):
        pass
    def get_right(self):
        pass
    def get_middle(self):
        pass
    def get_line_word(self):
        pass

if __name__ == "__main__":
    print("Quick dev testing for sensors!")

    ultra = Ultrasonic()
    while True:
        print("Distance (cm):", ultra.get_cm())
        time.sleep(1)
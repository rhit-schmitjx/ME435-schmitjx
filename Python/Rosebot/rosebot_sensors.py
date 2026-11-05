import gpiozero as gz
import time
class Ultrasonic:
    def __init__(self):
        self.sensor = gz.DistanceSensor(echo=22, trigger=27)

    def get_cm(self):
        return self.sensor.distance * 100

class LineSensors:
    def __init__(self, port):
        self.left = gz.LineSensor(14)
        self.right = gz.LineSensor(23)
        self.middle = gz.LineSensor(15)

    def get_left(self):
        if self.left.value==1:
            return "B"
        else:
            return "W"

    def get_right(self):
        if self.right.value==1:
            return "B"
        else:
            return "W"

    def get_middle(self):
        if self.middle.value==1:
            return "B"
        else:
            return "W"

    def get_line_word(self):
        left = self.get_left()
        right = self.get_right()
        middle = self.get_middle()
        return f"{left}{middle}{right}"

if __name__ == "__main__":
    print("Quick dev testing for sensors!")

    ultra = Ultrasonic()
    while True:
        # print("Distance (cm):", ultra.get_cm())
        print("Line Sensors:", LineSensors(0).get_line_word())
        
        time.sleep(1)
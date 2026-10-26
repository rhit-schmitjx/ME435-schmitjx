import gpiozero as gz
from rosebot_drive_system import DriveSystem

class Rosebot:
    def __init__(self):
        self.drive_system = DriveSystem()
        self.leds = None
        self.ultrasonic = None
        self.line_sensors = None
        self.servo_head = None
        self.buzzer = gz.Buzzer(17)
        self.adc = None
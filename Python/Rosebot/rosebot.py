import gpiozero as gz
from rosebot_drive_system import DriveSystem
import rosebot_sensors
import led


class Rosebot:
    def __init__(self):
        self.drive_system = DriveSystem()
        self.leds = led.LED()
        self.ultrasonic = rosebot_sensors.Ultrasonic()
        self.line_sensors = rosebot_sensors.LineSensors()
        self.servo_head = None
        self.buzzer = gz.Buzzer(17)
        self.adc = rosebot_sensors.ADC()
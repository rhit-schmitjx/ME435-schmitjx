import time
import sys
import gpiozero as gz
import mqtt_helper as mh
import threading
from datetime import datetime


class App:
    def __init__(self):
        self.IN1 = gz.OutputDevice(17)
        self.IN2 = gz.OutputDevice(18)
        self.IN3 = gz.OutputDevice(27)
        self.IN4 = gz.OutputDevice(22)

        self.STEP_SEQUENCE = [
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1],
            [1, 0, 0, 1]]
        self.STEPS_PER_REV = 4096

        self.open_deg = 360.0*6
        self.alarm_hour = 17
        self.alarm_minute = 59
        self.alarm_triggered = False

    def set_pins(self, step):
        self.IN1.value = step[0]
        self.IN2.value = step[1]
        self.IN3.value = step[2]
        self.IN4.value = step[3]

    def motor_off(self):
        self.IN1.off()
        self.IN2.off()
        self.IN3.off()
        self.IN4.off()

    def rotate(self, degrees):
        num_steps = int((abs(degrees) / 360.0) * self.STEPS_PER_REV)
        if degrees > 0:
            direction = 1
        else:
            direction = -1
        print(f"--Moving {degrees} degrees--")

        i = 0
        for _ in range(num_steps):
            self.set_pins(self.STEP_SEQUENCE[i])
            time.sleep(0.0012)
            i = (i + direction) % len(self.STEP_SEQUENCE)

        self.motor_off()
        print("--Done--")

    def alarm_checker(self):
        print(f"Alarm clock set for {self.alarm_hour:02d}:{self.alarm_minute:02d}")
        while True:
            now = datetime.now()
            if now.hour == self.alarm_hour and now.minute == self.alarm_minute:
                if not self.alarm_triggered:
                    print(f"\n[ALARM] -- Time is {now.strftime('%H:%M')}. Opening blinds --")
                    self.rotate(self.open_deg)
                    self.alarm_triggered = True
            else:
                if self.alarm_triggered:
                    self.alarm_triggered = False
                    
            time.sleep(1)

    def set_alarm(self, hour, minute):
        """Updates the alarm time dynamically from the web interface."""
        self.alarm_hour = int(hour)
        self.alarm_minute = int(minute)
        self.alarm_triggered_today = False  # Reset so it triggers at the new time
        print(f"Alarm updated to {self.alarm_hour:02d}:{self.alarm_minute:02d}")

    def terminal_listener(self):
        print("Type 'open', 'close', ##, or 'exit':")
        print("------------------------------------------------------")
        while True:
            command = input("\nEnter command: ")
            
            if command == 'exit':
                print("Exiting...")
                self.motor_off()
                sys.exit(0)
                KeyboardInterrupt
            elif command == 'open':
                self.rotate(self.open_deg)
            elif command == 'close':
                self.rotate(-self.open_deg)
            else:
                try:
                    deg = float(command)
                    self.rotate(deg)
                except ValueError:
                    print("**Invalid input. Please enter a number (e.g. 90, -45) or 'open'/'close'/'exit'.**")

def main():
    app = App()
    t_terminal = threading.Thread(target=app.terminal_listener, daemon=True)
    t_terminal.start()
    t_alarm = threading.Thread(target=app.alarm_checker, daemon=True)
    t_alarm.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        app.motor_off()
        print("\nSafely shut down.")

if __name__ == "__main__":
    main()
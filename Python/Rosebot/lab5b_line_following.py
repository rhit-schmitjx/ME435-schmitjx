from rosebot import Rosebot
import time
def main():
    print("Lab 5b Line Following")
    robot = Rosebot()

    try:
        while True:
            # Get ultrasonic sensor
            # if distance < 20 cm
            #    stop the robot
            # else
            #    get the line sensor values
            #    Adjust wheel speeds based on YOUR strategy



            time.sleep(0.1)

    except KeyboardInterrupt:
        # handle crtl-c to exit the program cleanly
        robot.drive_system.stop()
        print("Goodbye!")

















main()
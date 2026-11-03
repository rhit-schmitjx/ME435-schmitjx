from rosebot import Rosebot
import time

def main():
    print("Lab 5b Line Following")
    robot = Rosebot()

    speed = 40
    turn = 25
    try:
        while True:
            line_word = robot.line_sensors.get_line_word()
            #straight
            if line_word == "WBW" or line_word == "BBB":
                robot.drive_system.set_speeds(speed, speed, speed, speed)
            #go right
            elif line_word == "BWW" or line_word == "BBW":
                robot.drive_system.set_speeds(speed - turn, speed - turn, speed + turn, speed + turn)
            # go left
            elif line_word == "WWB" or line_word == "WBB":
                robot.drive_system.set_speeds(speed + turn, speed + turn, speed - turn, speed - turn)
            # stop
            else:
                robot.drive_system.set_speeds(0,0,0,0)


    except KeyboardInterrupt:
        robot.drive_system.stop()
        print("\nGoodbye!")

if __name__ == "__main__":
    main()
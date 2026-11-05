from rosebot import Rosebot
import time

def main():
    print("Lab 5b Line Following - Pivot Turns")
    robot = Rosebot()

    forward_speed = 15
    turn_speed = 15

    try:
        while True:
            line_word = robot.line_sensors.get_line_word()
            
            # Straight
            if line_word == "WBW" or line_word == "BBB":
                robot.drive_system.set_speeds(forward_speed, forward_speed, forward_speed, forward_speed)
                
            # left
            elif line_word == "BWW" or line_word == "BBW":
                robot.drive_system.set_speeds(0, 0, turn_speed, turn_speed)
                
            # Right
            elif line_word == "WWB" or line_word == "WBB":
                robot.drive_system.set_speeds(turn_speed, turn_speed, 0, 0)
    
            else:
                robot.drive_system.set_speeds(0, 0, 0, 0)

            time.sleep(0.02)

    except KeyboardInterrupt:
        robot.drive_system.stop()
        print("\nGoodbye!")

if __name__ == "__main__":
    main()
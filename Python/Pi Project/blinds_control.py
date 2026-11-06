import time
import sys
from gpiozero import gz

# Define GPIO Pins (BCM numbering) connected to ULN2003 IN1-IN4
IN1 = gz(17)
IN2 = gz(18)
IN3 = gz(27)
IN4 = gz(22)

# Step sequence for 28BYJ-48 in Half-Step mode (8-step sequence for smooth rotation)
STEP_SEQUENCE = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

# The 28BYJ-48 with 1/64 gear reduction requires ~4096 half-steps per full 360-degree rotation.
STEPS_PER_REV = 4096

def set_pins(step):
    """Sets the GPIO pins according to the active step state."""
    IN1.value = step[0]
    IN2.value = step[1]
    IN3.value = step[2]
    IN4.value = step[3]

def motor_off():
    """De-energizes all motor coils to save power and prevent heat buildup."""
    IN1.off()
    IN2.off()
    IN3.off()
    IN4.off()

def rotate(degrees):
    """
    Rotates the stepper motor by a specified angle in degrees.
    :param degrees: Positive for clockwise (open/tilt up), negative for counter-clockwise (close/tilt down)
    """
    steps_to_take = int((abs(degrees) / 360.0) * STEPS_PER_REV)
    if degrees > 0: direction = 1
    else: direction = -1

    print(f"**Moving {degrees} degrees**")

    i = 0
    for i in range(steps_to_take):
        set_pins(STEP_SEQUENCE[i])
        time.sleep(0.002)
        i = (i + direction) % len(STEP_SEQUENCE)

    # Cut power to motor when done turning so it doesn't stay hot
    motor_off()
    print("---Done---")

def main():
    print("Commands:")
    print("  Type a degree number to move (e.g., '90', '-90', '45', '-180')")
    print("  'open'  -> Tilts blinds open (+90 degrees)")
    print("  'close' -> Tilts blinds closed (-90 degrees)")
    print("  'exit' -> Close program")
    print("------------------------------------------------------")

    try:
        while True:
            command = input("\nEnter command: ")
            
            if command == 'exit':
                print("Exiting...")
                break
            elif command == 'open':
                rotate(90)
            elif command == 'close':
                rotate(-90)
            else:
                try:
                    deg = float(command)
                    rotate(deg)
                except ValueError:
                    print("**Invalid input. Please enter a number (e.g. 90, -45) or 'open'/'close'/'exit'.**")

    except KeyboardInterrupt:
        print("\nProgram interrupted.")
    finally:
        motor_off()
        print("Motor pins released safely.")

if __name__ == "__main__":
    main()
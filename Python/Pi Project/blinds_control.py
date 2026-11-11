import time
import sys
import gpiozero as gz
import mqtt_helper as mh
import threading


class App:
    def __init__(self):
        # Define GPIO Pins (BCM numbering) connected to ULN2003 IN1-IN4
        self.IN1 = gz.OutputDevice(17)
        self.IN2 = gz.OutputDevice(18)
        self.IN3 = gz.OutputDevice(27)
        self.IN4 = gz.OutputDevice(22)

        # Step sequence for 28BYJ-48 in Half-Step mode (8-step sequence for smooth rotation)
        self.STEP_SEQUENCE = [
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
        self.STEPS_PER_REV = 4096

        # Setup MQTT Client (which receives payloads from your bridge/Alexa)
        # self.mqtt_client = mh.MqttClient()
        # self.mqtt_client.connect(
        #     subscription_topic_name="me435/schmitjx/#",
        #     publish_topic_name="me435/schmitjx/to_computer"
        # )
        # self.mqtt_client.callback = self.mqtt_callback

    def set_pins(self, step):
        """Sets the GPIO pins according to the active step state."""
        self.IN1.value = step[0]
        self.IN2.value = step[1]
        self.IN3.value = step[2]
        self.IN4.value = step[3]

    def motor_off(self):
        """De-energizes all motor coils to save power and prevent heat buildup."""
        self.IN1.off()
        self.IN2.off()
        self.IN3.off()
        self.IN4.off()

    def rotate(self, degrees):
        """
        Rotates the stepper motor by a specified angle in degrees.
        :param degrees: Positive for clockwise (open/tilt up), negative for counter-clockwise (close/tilt down)
        """
        steps_to_take = int((abs(degrees) / 360.0) * self.STEPS_PER_REV)
        if degrees > 0: direction = 1
        else: direction = -1

        print(f"**Moving {degrees} degrees**")

        i = 0
        for _ in range(steps_to_take):
            self.set_pins(self.STEP_SEQUENCE[i])
            time.sleep(0.0012)
            i = (i + direction) % len(self.STEP_SEQUENCE)

        # Cut power to motor when done turning so it doesn't stay hot
        self.motor_off()
        print("---Done---")

    def mqtt_callback(self, message_type, message_payload):
        print(f"Alexa Received! --> Type: {message_type} | Payload: {message_payload}")
        if message_type == "blinds":
            if message_payload == "open":
                self.rotate_degrees(90)
            elif message_payload == "close":
                self.rotate_degrees(-90)
    def terminal_listener(self):
        print("Commands:")
        print("  Type a degree number to move (e.g., '90', '-90', '45', '-180')")
        print("  'open'  -> Tilts blinds open (+90 degrees)")
        print("  'close' -> Tilts blinds closed (-90 degrees)")
        print("  'exit' -> Close program")
        print("------------------------------------------------------")

        
        while True:
            command = input("\nEnter command: ")
            
            if command == 'exit':
                print("Exiting...")
                self.release_motor()
                sys.exit(0)
            elif command == 'open':
                self.rotate(90)
            elif command == 'close':
                self.rotate(-90)
            else:
                try:
                    deg = float(command)
                    self.rotate(deg)
                except ValueError:
                    print("**Invalid input. Please enter a number (e.g. 90, -45) or 'open'/'close'/'exit'.**")

def main():
    app = App()

    # Start the terminal input loop in a separate background thread
    t = threading.Thread(target=app.terminal_listener, daemon=True)
    t.start()
    # Keep the main thread alive to listen for incoming MQTT/Alexa payloads
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        app.release_motor()
        print("\nSafely shut down.")

if __name__ == "__main__":
    main()
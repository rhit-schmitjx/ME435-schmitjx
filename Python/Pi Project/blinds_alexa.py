import time
import sys
import threading
import gpiozero as gz
from sinricpro import SinricPro
from sinricpro.device.blinds import SinricProBlinds

class App:
    def __init__(self):
        # Setup motor output pins
        self.in1 = gz.OutputDevice(17)
        self.in2 = gz.OutputDevice(18)
        self.in3 = gz.OutputDevice(27)
        self.in4 = gz.OutputDevice(22)

        self.step_sequence = [
            [1, 0, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0],
            [0, 0, 1, 0], [0, 0, 1, 1], [0, 0, 0, 1], [1, 0, 0, 1]
        ]
        self.steps_per_rev = 4096

    def set_pins(self, step):
        self.in1.value = step[0]
        self.in2.value = step[1]
        self.in3.value = step[2]
        self.in4.value = step[3]

    def release_motor(self):
        self.in1.off()
        self.in2.off()
        self.in3.off()
        self.in4.off()

    def rotate_degrees(self, degrees, speed_delay=0.0012):
        steps_to_take = int((abs(degrees) / 360.0) * self.steps_per_rev)
        direction = 1 if degrees > 0 else -1
        
        print(f"\n[*] Moving {degrees}° ({steps_to_take} steps)...")
        step_idx = 0
        for _ in range(steps_to_take):
            self.set_pins(self.step_sequence[step_idx])
            time.sleep(speed_delay)
            step_idx = (step_idx + direction) % len(self.step_sequence)

        self.release_motor()
        print("[+] Done. Enter command > ", end="", flush=True)

    # --- Sinric Pro Callbacks (Triggered by Alexa) ---
    def handle_open_close(self, device_id, position):
        """Triggered when Alexa commands the blinds to open/close or set a percentage."""
        print(f"\n[Alexa Trigger] Target position received: {position}%")
        # If position is close to 100 (Open), rotate +90 degrees. If 0 (Closed), rotate -90 degrees.
        if position > 50:
            self.rotate_degrees(90)
        else:
            self.rotate_degrees(-90)
        return True

    def terminal_listener(self):
        """Allows typing commands locally in the terminal concurrently."""
        print("Commands: Type degrees (e.g. '90', '-90'), 'open', 'close', or 'q' to quit.")
        while True:
            cmd = input("Enter command > ").strip().lower()
            if cmd in ['q', 'exit', 'quit']:
                print("Exiting...")
                self.release_motor()
                sys.exit(0)
            elif cmd == 'open':
                self.rotate_degrees(90)
            elif cmd == 'close':
                self.rotate_degrees(-90)
            else:
                try:
                    deg = float(cmd)
                    self.rotate_degrees(deg)
                except ValueError:
                    print("[!] Invalid input.")

def main():
    app = App()

    # Configure Sinric Pro Device
    device_id = '6af40a596d3b5ef5cdaf71ed'
    blinds_device = SinricProBlinds(device_id)
    
    # Bind Alexa command callbacks to your python function
    blinds_device.on_range_value(app.handle_open_close) # Or on_power_state if configured as switch

    # Initialize Sinric Pro client
    app_key = 'e87533a6-cb8e-44f6-9b77-fcf3d6ead78a'
    app_secret = '990d1942-69ce-4e7d-9e98-9bbde73feae7-8c0096d9-7d64-4900-888d-ba19be401f08'
    
    client = SinricPro(app_key, app_secret, [blinds_device], restore_device_states=False)

    # Start the terminal input loop in a separate background thread
    terminal_thread = threading.Thread(target=app.terminal_listener, daemon=True)
    terminal_thread.start()

    print("Starting Sinric Pro client listener...")
    try:
        client.run()
    except KeyboardInterrupt:
        app.release_motor()
        print("\nSafely shut down.")

if __name__ == "__main__":
    main()
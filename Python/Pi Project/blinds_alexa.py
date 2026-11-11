import time
import sys
import threading
import asyncio
import gpiozero as gz
from sinricpro import SinricPro, SinricProBlinds, SinricProConfig

class BlindApp:
    def __init__(self):
        try:
            self.in1 = gz.OutputDevice(17)
            self.in2 = gz.OutputDevice(18)
            self.in3 = gz.OutputDevice(27)
            self.in4 = gz.OutputDevice(22)
        except Exception:
            pass

        self.step_sequence = [
            [1, 0, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0],
            [0, 0, 1, 0], [0, 0, 1, 1], [0, 0, 0, 1], [1, 0, 0, 1]
        ]
        self.steps_per_rev = 4096 
        self.current_position = 0
        self.max_tilt_degrees = 4 * 360.0  

    def set_pins(self, step):
        self.in1.value = step[0]
        self.in2.value = step[1]
        self.in3.value = step[2]
        self.in4.value = step[3]

    def release_motor(self):
        try:
            self.in1.off()
            self.in2.off()
            self.in3.off()
            self.in4.off()
        except Exception:
            pass

    def rotate_degrees(self, degrees, speed_delay=0.0012):
        steps_to_take = int((abs(degrees) / 360.0) * self.steps_per_rev)
        direction = 1 if degrees > 0 else -1
        
        print(f"\n[*] Rotating {degrees}° ({steps_to_take} steps)...")
        step_idx = 0
        for _ in range(steps_to_take):
            self.set_pins(self.step_sequence[step_idx])
            time.sleep(speed_delay)
            step_idx = (step_idx + direction) % len(self.step_sequence)

        self.release_motor()
        print("[+] Rotation complete.")

    def move_to_percentage(self, target_percentage):
        target_percentage = max(0, min(100, target_percentage))
        target_degrees = (target_percentage / 100.0) * self.max_tilt_degrees
        current_degrees = (self.current_position / 100.0) * self.max_tilt_degrees
        
        delta_degrees = target_degrees - current_degrees
        
        if delta_degrees != 0:
            self.rotate_degrees(delta_degrees)
            self.current_position = target_percentage
            print(f"[Sync] Blinds position updated to: {self.current_position}%")

    def terminal_listener(self):
        print("\n--- Local Terminal Ready ---")
        print("Commands: Type degrees (e.g. '45', '-45'), 'open', 'close', or 'q' to quit.")
        while True:
            try:
                cmd = input("\nEnter command > ").strip().lower()
                if cmd in ['q', 'exit', 'quit']:
                    print("Exiting...")
                    self.release_motor()
                    sys.exit(0)
                elif cmd == 'open':
                    self.move_to_percentage(100)
                elif cmd == 'close':
                    self.move_to_percentage(0)
                else:
                    try:
                        deg = float(cmd)
                        self.rotate_degrees(deg)
                        print(f"[+] Moved {deg}° manually.")
                    except ValueError:
                        print("[!] Invalid input. Enter a number, 'open', 'close', or 'q'.")
            except Exception as e:
                print(f"[!] Terminal Error: {e}")


def main():
    app = BlindApp()

    DEVICE_ID = "6af40a596d3b5ef5cdaf71ed"
    APP_KEY = "e87533a6-cb8e-44f6-9b77-fcf3d6ead78a"
    APP_SECRET = "990d1942-69ce-4e7d-9e98-9bbde73feae7-8c0096d9-7d64-4900-888d-ba19be401f08"

    blinds = SinricProBlinds(DEVICE_ID)

    def on_open_close(device_id, position: int) -> bool:
        print(f"\n[Alexa Voice Command] Target position: {position}%")
        app.move_to_percentage(position)
        return True

    def on_power_state(device_id, state: bool) -> bool:
        print(f"\n[Alexa Voice Command] Motor Power: {'ON' if state else 'OFF'}")
        return True

    blinds.on_open_close(on_open_close)
    blinds.on_power_state(on_power_state)

    # Initialize configuration and singleton once
    config = SinricProConfig(app_key=APP_KEY, app_secret=APP_SECRET)
    sinric_pro = SinricPro.get_instance()
    sinric_pro.add(blinds)

    # Start the terminal listener thread
    terminal_thread = threading.Thread(target=app.terminal_listener, daemon=True)
    terminal_thread.start()

    print("Starting Sinric Pro client listener...")
    
    # Run a single clean asyncio loop. Let the library manage its connection state.
    try:
        asyncio.run(sinric_pro.begin(config))
    except KeyboardInterrupt:
        app.release_motor()
        print("\nSafely shut down.")


if __name__ == "__main__":
    main()
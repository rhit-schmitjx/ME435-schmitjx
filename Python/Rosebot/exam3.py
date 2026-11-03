import threading
import time
import mqtt_helper as mh
from rosebot import Rosebot


class App:

  def __init__(self):
    self.robot = Rosebot()

    self.mqtt_client = mh.MqttClient()
    self.mqtt_client.connect(
        subscription_topic_name="me435/schmitjx/#",
        publish_topic_name="me435/schmitjx/to_computer",
    )
    self.mqtt_client.callback = self.mqtt_callback

    # Start a background daemon thread to stream ultrasonic data every 2 seconds
    self.ultra_thread = threading.Thread(
        target=self.ultra_publisher_loop, daemon=True
    )
    self.ultra_thread.start()

  def mqtt_callback(self, message_type, message_payload):
    print("Received type:", message_type)
    print("Received payload:", message_payload)

    try:
      if message_type == "left":
        # payload format: [forward_reverse, time, speed]
        direction, t, speed = message_payload
        print(f"Side: Left | Direction: {direction} | Time: {t} | Speed: {speed}")

        # Scale speed (-100 to 100) to duty cycle and run for 't' seconds
        scaled = self.robot.drive_system.scale_speed(speed)
        if direction == 0:  # reverse
          scaled = -scaled

        # Apply to left side motors (Left Front and Left Rear)
        self.robot.drive_system.car.set_motor_model(
            scaled, scaled, 0, 0
        )  # adjust based on motor layout model
        time.sleep(t)
        self.robot.drive_system.stop()

      elif message_type == "right":
        # payload format: [forward_reverse, time, speed]
        direction, t, speed = message_payload
        print(f"Side: Right | Direction: {direction} | Time: {t} | Speed: {speed}")

        scaled = self.robot.drive_system.scale_speed(speed)
        if direction == 0:
          scaled = -scaled

        # Apply to right side motors (Right Front and Right Rear)
        self.robot.drive_system.car.set_motor_model(0, 0, scaled, scaled)
        time.sleep(t)
        self.robot.drive_system.stop()

      elif message_type == "both":
        # payload format: [forward_reverse, time, left_speed, right_speed]
        direction, t, left_speed, right_speed = message_payload
        print(f"Side: Both | Direction: {direction} | Time: {t} | Speed Left: {left_speed} | Speed Right: {right_speed}")

        left_scaled = self.robot.drive_system.scale_speed(left_speed)
        right_scaled = self.robot.drive_system.scale_speed(right_speed)

        if direction == 0:
          left_scaled = -left_scaled
          right_scaled = -right_scaled

        self.robot.drive_system.car.set_motor_model(
            left_scaled, left_scaled, right_scaled, right_scaled
        )
        time.sleep(t)
        self.robot.drive_system.stop()

    except Exception as e:
      print(f"Error executing command: {e}")

  def ultra_publisher_loop(self):
    while True:
      try:
        # Read ultrasonic sensor distance (adjust method depending on your rosebot sensor library implementation)
        distance_cm = self.robot.ultrasonic.get_distance()
        print(f"Ultra: {distance_cm}")

        # Send via MQTT helper using the requested schema {"type": "ultra", "payload": ...}
        self.mqtt_client.send_message("ultra", distance_cm)
      except Exception as e:
        print(f"Error reading/publishing ultrasonic sensor: {e}")

      time.sleep(2)


def main():
  print("Exam 3 Tank MQTT Car Running")
  app = App()
  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    print("Goodbye!")
    app.robot.drive_system.stop()
    app.mqtt_client.close()


if __name__ == "__main__":
  main()
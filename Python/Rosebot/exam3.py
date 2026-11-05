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

    self.last_ultra_time = time.time()

  def mqtt_callback(self, message_type, message_payload):
    print("Received type:", message_type)
    print("Received payload:", message_payload)

    if message_type == "left":
      direction, t, speed = message_payload
      print(f"Side: Left | Direction: {direction} | Time: {t} | Speed: {speed}")

      scaled_speed = self.robot.drive_system.scale_speed(speed)
      if direction == 0:
        scaled_speed = -scaled_speed

      self.robot.drive_system.car.set_motor_model(scaled_speed, scaled_speed, 0, 0)
      time.sleep(t)
      self.robot.drive_system.stop()

    elif message_type == "right":
      direction, t, speed = message_payload
      print(
          f"Side: Right | Direction: {direction} | Time: {t} | Speed: {speed}")

      scaled_speed = self.robot.drive_system.scale_speed(speed)
      if direction == 0:
        scaled_speed = -scaled_speed

      self.robot.drive_system.car.set_motor_model(0, 0, scaled_speed, scaled_speed)
      time.sleep(t)
      self.robot.drive_system.stop()

    elif message_type == "both":
      direction, t, left_speed, right_speed = message_payload
      print(
          f"Side: Both | Direction: {direction} | Time: {t} | Speed Left: {left_speed} | Speed Right: {right_speed}"
      )

      left_scaled = self.robot.drive_system.scale_speed(left_speed)
      right_scaled = self.robot.drive_system.scale_speed(right_speed)

      if direction == 0:
        left_scaled = -left_scaled
        right_scaled = -right_scaled

      self.robot.drive_system.car.set_motor_model(left_scaled, left_scaled, right_scaled, right_scaled)
      time.sleep(t)
      self.robot.drive_system.stop()

  def check_ultra(self):
    current_time = time.time()
    if current_time - self.last_ultra_time >= 2.0:
      try:
        distance_cm = self.robot.ultrasonic.get_distance()
        print(f"Ultra: {distance_cm}")
        self.mqtt_client.send_message("ultra", distance_cm)
      except Exception:
        print(f"No ultrasonic sensor")
      
      self.last_ultra_time = current_time


def main():
  print("Exam 3")
  app = App()
  try:
    while True:
      app.check_ultra()

      time.sleep(0.1)

  except KeyboardInterrupt:
    print("Goodbye!")
    app.robot.drive_system.stop()
    app.mqtt_client.close()


if __name__ == "__main__":
  main()
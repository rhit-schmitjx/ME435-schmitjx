import mqtt_helper as mh
import signal
import time


class App:

    def __init__(self):
        #TODO: Setup LED's
        #TODO: Setup pushbuttons

        self.mqtt_client = mh.Mqtt.Client()
        self.mqtt_client.connect(subscription_topic_name="me435/schmitjx/#",
                                 publish_topic_name="me435/schmitjx/to_computer")

    def mqtt_callback(self, message_type, message_payload):
        print("Received type:", message_type)
        print("Received payload:", message_payload)

def main():
    print("GPIO MQTT")
    app = App()

    while True:
        # Send test messge!
        app.mqtt_client.send_message("red","on")
        time.sleep(1)
        app.mqtt_client.send_message("red","off")
        time.sleep()


















main()
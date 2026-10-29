import mqtt_helper as mh
import gpiozero as gz
import signal
import time


class App:

    def __init__(self):
        #TODO: Setup LED's
        #TODO: Setup pushbuttons

        self.red_led = gz.LED(14)
        self.blue_led = gz.LED(15)
        self.green_led = gz.LED(18)
        
        self.button23 = gz.Button(23)
        self.button25 = gz.Button(25)

        self.mqtt_client = mh.MqttClient()
        self.mqtt_client.connect(subscription_topic_name="me435/schmitjx/#",
                                 publish_topic_name="me435/schmitjx/to_computer")
        self.mqtt_client.callback = self.mqtt_callback
        
        self.button23.when_pressed = lambda: self.mqtt_client.send_message("button")
        self.button25.when_pressed = lambda: self.mqtt_client.send_message("reset")

    def mqtt_callback(self, message_type, message_payload):
        print("Received type:", message_type)
        print("Received payload:", message_payload)

        if message_type == "red":
            if message_payload == "on":
                self.red_led.on()
                print("hi")
            elif message_payload == "off":
                self.red_led.off()

        if message_type == "blue":
            if message_payload == "on":
                self.blue_led.on()
            elif message_payload == "off":
                self.blue_led.off()

        if message_type == "green":
            if message_payload == "on":
                self.green_led.on()
            elif message_payload == "off":
                self.green_led.off()

        if message_type == "leds":
            if message_payload[0] == "on":
                self.red_led.on()
            else:
                self.red_led.off()
            if message_payload[1] == "on":
                self.blue_led.on()
            else:
                self.blue_led.off()

            if message_payload[2] == "on":
                self.green_led.on()
            else:
                self.green_led.off()


def main():
    print("GPIO MQTT")
    app = App()

    while True:
        # Send test messge!
        # app.mqtt_client.send_message("red","on")
        # app.mqtt_client.send_message("blue","on")
        # app.mqtt_client.send_message("green","on")
        app.mqtt_client.send_message("leds", ["on", "off", "on"])
        time.sleep(0.5)
        # app.mqtt_client.send_message("red","off")
        # app.mqtt_client.send_message("blue","off")
        # app.mqtt_client.send_message("green","off")
        app.mqtt_client.send_message("leds", ["off", "on", "off"])
        time.sleep(0.5)


















main()
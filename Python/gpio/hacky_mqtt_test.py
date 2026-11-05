import mqtt_helper as mh
import time

def my_callback(message_type, payload):
    print("The message type is " + message_type)
    print("The message payload is " + str(payload))

def main():
    print("Hacky MQTT test")
    mqtt_client = mh.MqttClient()
    mqtt_client.connect(subscription_topic_name="schmitjx",publish_topic_name="schmitjx",use_off_campus_broker=True)
    mqtt_client.callback = my_callback

    counter=0
    while True:
        mqtt_client.send_message("counter", counter)
        time.sleep(2)
        counter += 1
















main()
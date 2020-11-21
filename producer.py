#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import logging

import config


LEFT_SENSOR_GPIO = 14
RIGHT_SENSOR_GPIO = 15
CHECK_INTERVAL = 5  # In seconds
logging.basicConfig(level=logging.DEBUG)

client = mqtt.Client()
client.username_pw_set(config.MQTT_USER, config.MQTT_PASSWORD)
client.connect(config.MQTT_HOST, 1883, 60)


class DoorSensor:
    def __init__(self, gpio, topic):
        self.gpio = gpio
        self.topic = topic
        GPIO.setup(self.gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def is_open(self):
        return GPIO.input(self.gpio)

    def is_closed(self):
        return not self.is_open()

    def get_state(self):
        return 'ON' if self.is_open() else 'OFF'

    def publish_state(self):
        state = self.get_state()
        client.publish(self.topic, state)
        logging.info("Published state %s on topic %s" % (state, self.topic))


def main():
    left_door = DoorSensor(LEFT_SENSOR_GPIO, 'home-assistant/garage-door-left/sensor')
    right_door = DoorSensor(RIGHT_SENSOR_GPIO, 'home-assistant/garage-door-right/sensor')

    while True:
        left_door.publish_state()
        right_door.publish_state()
        time.sleep(CHECK_INTERVAL)


def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)


if __name__ == '__main__':
    setup_gpio()
    main()

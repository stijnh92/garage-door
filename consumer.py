#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import logging

import config


TOPICS = [
    ('home-assistant/garage-door-left/set', 1),
    ('home-assistant/garage-door-right/set', 1)
]
LEFT_RELAY_GPIO = 27
RIGHT_RELAY_GPIO = 17
logging.basicConfig(level=logging.DEBUG)


def on_connect(client, userdata, flags, rc):
    print("Connected to host %s" % config.MQTT_HOST)
    client.subscribe(TOPICS)
    print("Subscribing to topics %s" % TOPICS)


def on_message(client, userdata, msg):
    logging.warning("Received new message: %s (%s)" % (msg.payload, msg.topic))

    if msg.topic == 'home-assistant/garage-door-left/set':
        toggle_door(LEFT_RELAY_GPIO)
    elif msg.topic == 'home-assistant/garage-door-right/set':
        toggle_door(RIGHT_RELAY_GPIO)


def toggle_door(pin):
    print('toggle garage door')
    GPIO.output(pin, False)
    time.sleep(0.3)
    GPIO.output(pin, True)
    logging.info('garage door has been toggled (gpio pin %s)' % pin)

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Output
    GPIO.setup(LEFT_RELAY_GPIO, GPIO.OUT)
    GPIO.setup(RIGHT_RELAY_GPIO, GPIO.OUT)

def connect_mqtt():
    client = mqtt.Client()
    client.username_pw_set(config.MQTT_USER, config.MQTT_PASSWORD)
    client.connect(config.MQTT_HOST, 1883, 60)

    client.on_connect = on_connect
    client.on_message = on_message

    client.loop_forever()

if __name__ == '__main__':
    setup_gpio()
    connect_mqtt()

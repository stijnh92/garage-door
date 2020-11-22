#!/usr/bin/python3

import smbus
import time

import paho.mqtt.client as mqtt

import config


bus = smbus.SMBus(1)
ADDRESS = 0x40

client = mqtt.Client()
client.username_pw_set(config.MQTT_USER, config.MQTT_PASSWORD)
client.connect(config.MQTT_HOST, 1883, 60)

TEMPERATURE_TOPIC = 'home-assistant/garage/temperature'
HUMIDITY_TOPIC = 'home-assistant/garage/humidity'
UPDATE_INTERVAL = 60  # Time in seconds

def read_data(value):
    bus.write_byte(ADDRESS, value)
    time.sleep(0.5)

    # read data back, 2bytes
    data0 = bus.read_byte(ADDRESS)
    data1 = bus.read_byte(ADDRESS)

    return data0, data1


def get_temperature():
    data0, data1 = read_data(0xF3)
    temp = data0 * 256 + data1
    return -46.85 + ((temp * 175.72) / 65536.0)


def get_humidity():
    data0, data1 = read_data(0xF5)
    humidity = data0 * 256 + data1
    return -6 + ((humidity * 125.0) / 65536.0)


def main():
    while True:
        client.publish(TEMPERATURE_TOPIC, '%.2f' % get_temperature())
        client.publish(HUMIDITY_TOPIC, '%.2f' % get_humidity())
        time.sleep(UPDATE_INTERVAL)


if __name__ == '__main__':
    main()

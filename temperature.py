#!/usr/bin/python3

import smbus
import time

bus = smbus.SMBus(1)
ADDRESS = 0x40


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


if __name__ == '__main__':
    temp = get_temperature()
    humidity = get_humidity()

    print("Temperature: ", '%.2f' % temp, "C")
    print("Humidity: ", '%.2f' % humidity, "%")

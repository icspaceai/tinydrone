from vpython import arrow, color, vector 
import serial
from time import sleep
import numpy as np


def create_arrows():
    arrow(length=2, shaftwidth=0.1, color=color.red, axis=vector(1, 0, 0))
    arrow(length=2, shaftwidth=0.1, color=color.green, axis=vector(0, 1, 0))
    arrow(length=2, shaftwidth=0.1, color=color.blue, axis=vector(0, 0, 1))
    
    imu_front_arrow = arrow(shaftwidth=0.1, color=color.yellow, axis=vector(1, 0, 0))
    imu_side_arrow = arrow(shaftwidth=0.1, color=color.orange, axis=vector(0, 1, 0))
    imu_up_arrow = arrow(length=1, shaftwidth=0.1, color=color.magenta, axis=vector(0, 0, 1))
    return (imu_front_arrow, imu_side_arrow, imu_up_arrow)


def init_imu_data(port):
    espData = serial.Serial(port, 115200)
    sleep(1)
    return espData


def get_imu_data(espData):
    toRad = 2 * np.pi / 360

    while espData.inWaiting() == 0:
        pass
    data = espData.readline()
    data = str(data, "utf-8")
    splitData = data.split("\t")
    yaw = float(splitData[0]) * toRad
    pitch = float(splitData[1]) * toRad
    roll = float(splitData[2]) * toRad
    return (yaw, pitch, roll)

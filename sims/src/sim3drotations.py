from vpython import scene, vector, cross, rate, box
import numpy as np
from math import sin, cos
from utils import create_arrows, init_imu_data, get_imu_data


class Sim3dRotationsModel():
    def __init__(self, serial_port="/dev/cu.SLAB_USBtoUART"):
        scene.title = "Drone 3D Rotations Simulator"
        scene.width = 650
        scene.height = 400
        scene.range = 1.3
        self.serial_port = serial_port


    def run_simulation(self):    
        (imuFrontArrow, imuSideArrow, imuUpArrow) = create_arrows()

        espData = init_imu_data(self.serial_port)

        bBoard = box(length=6, width=2, height=0.2, opacity=0.2, pos=vector(0, 0, 0))

        while True:
            (yaw, pitch, roll) = get_imu_data(espData)
            print(yaw, roll, pitch)

            rate(50)
            k = vector(cos(yaw) * cos(pitch), sin(pitch), sin(yaw) * cos(pitch))

            y = vector(0, 1, 0)
            s = cross(k, y)
            v = cross(s, k)
            vr = v * cos(roll) + cross(k, v) * sin(roll)
            bBoard.axis = k
            bBoard.up = vr

            imuFrontArrow.length = 4
            imuSideArrow.length = 2
            imuFrontArrow.axis = cross(k, vr)
            imuUpArrow.axis = v
            imuSideArrow.axis = s
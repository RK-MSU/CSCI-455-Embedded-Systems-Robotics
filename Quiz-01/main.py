'''
River Kelly
CSCI-455: Embedded Systems (Robotics)
Quiz 01
March 9, 2022
'''

from controller import Robot, Motor, DistanceSensor, Compass, TouchSensor
from enum import Enum
import math
import logging as log

LOG_LEVEL = log.DEBUG
LOG_LEVEL = log.INFO
TIME_STEP = 64
MAX_SPEED = 6.28

log.basicConfig(format='%(levelname)s: %(message)s', level=LOG_LEVEL)


class Direction(Enum):
    North = 'North'
    South = 'South'
    East = 'East'
    West = 'West'
    Left = 'Left'
    Right = 'Right'


def getRobotDevice(name: str):
    global robot
    device = None
    try:
        device = robot.getDevice(name)
    except:
        print("Unable to get Device: '{!s}'".format(name))
        return None
    if isinstance(device, Motor):
        device.setPosition(float('inf'))
        device.setVelocity(0.0)
    if isinstance(device, DistanceSensor) or isinstance(device, Compass) or isinstance(device, TouchSensor):
        device.enable(TIME_STEP)
    return device


def bearing():
    global compass
    if compass is None:
        return None
    dir = compass.getValues()
    if math.isnan(dir[0]):
        return None
    rad = math.atan2(dir[0], dir[1])
    bearing = (rad - 1.5708) / math.pi * 180.0
    if bearing < 0.0:
        bearing = bearing + 360.0
    return bearing


def direction():
    global bearing
    b = bearing()
    if b is None:
        return None
    if 45 < b <= 135:
        return Direction.West
    elif 135 < b <= 225:
        return Direction.South
    elif 225 < b <= 315:
        return Direction.East
    else:
        return Direction.North


def setSpeed(speed: int):
    global leftMotor
    global rightMotor
    speed = int(speed)
    if speed > 100:
        speed = 100
    elif speed < 0:
        speed = 0
    speed = MAX_SPEED * (speed / 100)
    leftMotor.setVelocity(speed)
    rightMotor.setVelocity(speed)


def printDebug():
    global robot, leftMotor, rightMotor, ps0, ps1, ps2, ps3, ps4, ps5, ps6, ps7, compass, touch
    print_str = "Time: {!s}\n"
    print_str += "Front Left: {:.2f} - Front Right: {:.2f}\n"
    print(print_str.format(
        robot.getTime(),
        ps0.getValue(),
        ps7.getValue()
    ))


robot: Robot = Robot()
leftMotor: Motor = getRobotDevice('left wheel motor')
rightMotor: Motor = getRobotDevice('right wheel motor')
ps0: DistanceSensor = getRobotDevice('ps0')
ps1: DistanceSensor = getRobotDevice('ps1')
ps2: DistanceSensor = getRobotDevice('ps2')
ps3: DistanceSensor = getRobotDevice('ps3')
ps4: DistanceSensor = getRobotDevice('ps4')
ps5: DistanceSensor = getRobotDevice('ps5')
ps6: DistanceSensor = getRobotDevice('ps6')
ps7: DistanceSensor = getRobotDevice('ps7')
compass: Compass = getRobotDevice('compass')
touch: TouchSensor = getRobotDevice("touch sensor")

setSpeed(100)

while robot.step(TIME_STEP) != -1:
    printDebug()

# END

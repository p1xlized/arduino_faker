import random

"""
Sensor data generation functions.
"""


def get_temp():
    return round(random.uniform(20.0, 30.0), 2)


def get_hum():
    return random.randint(30, 70)


def get_light():
    return random.randint(0, 1023)


def get_soil_moist():
    return random.randint(300, 650)


def get_dist_cm():
    return random.randint(5, 300)


def get_lidar_m():
    return round(random.uniform(0.1, 10.0), 3)

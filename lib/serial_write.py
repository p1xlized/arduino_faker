import serial

"""
Write a payload to the serial port.

:param ser: The serial port to write to.
:param payload: The payload to write.
"""


def write_to_serial(ser: serial.Serial, payload: str):
    ser.write(payload.encode())

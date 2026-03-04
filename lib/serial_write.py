import serial


def write_to_serial(ser: serial.Serial, payload: str):
    ser.write(payload.encode())

import random
import re
import time

import serial

from lib.open_socket import open_socket

# 1. Start the bridge and get output
terminal_output, socat_process = open_socket()

# 2. Extract ports using Regex
# findall(pattern, string)
ports = re.findall(r"/dev/pts/\d+", str(terminal_output))

if len(ports) < 2:
    print("Failed to find ports. Is socat installed?")
    if socat_process:
        socat_process.kill()
    exit()

ARDUINO_PORT = ports[0]
LISTENER_PORT = ports[1]

print(f"--- VIRTUAL BRIDGE ACTIVE ---")
print(f"Arduino (Sender) on: {ARDUINO_PORT}")
print(f"Analyzer (Receiver) on: {LISTENER_PORT}")
print(f"-----------------------------\n")

try:
    with serial.Serial(ARDUINO_PORT, 9600, timeout=1) as ser:
        while True:
            # Create a CSV-style string: Temp, Humidity, Light
            temp = round(random.uniform(20.0, 30.0), 2)
            hum = random.randint(30, 70)
            light = random.randint(0, 1023)

            payload = f"{temp},{hum},{light}\n"
            ser.write(payload.encode("utf-8"))

            print(f"Arduino Sent: {payload.strip()}")
            time.sleep(0.5)

except KeyboardInterrupt:
    print("\nShutting down...")
finally:
    if socat_process:
        socat_process.terminate()

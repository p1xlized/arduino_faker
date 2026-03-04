import platform  # Added to check OS
import random
import time

import serial

from lib.open_socket import get_ports, open_socket
from lib.serial_write import write_to_serial

# 1. Start the bridge and get output
# The library now handles the OS-specific logic
terminal_output, socat_process = open_socket()

# 2. Logic to assign ports based on OS
current_os = platform.system()

if current_os == "Windows":
    # On Windows, we assume you've set up a bridge like COM1 <-> COM2
    ARDUINO_PORT = "COM1"
    LISTENER_PORT = "COM2"
    print(f"--- WINDOWS MODE: Using pre-defined COM ports ---")
else:
    # On Linux/Mac, we parse the socat output
    ports = get_ports(terminal_output)

    if len(ports) < 2:
        print("Failed to find virtual ports. Is socat installed?")
        if socat_process:
            socat_process.kill()
        exit()

    ARDUINO_PORT = ports[0]
    LISTENER_PORT = ports[1]
    print(f"--- VIRTUAL BRIDGE ACTIVE ({current_os}) ---")

print(f"Arduino (Sender) on: {ARDUINO_PORT}")
print(f"Analyzer (Receiver) on: {LISTENER_PORT}")
print(f"-----------------------------\n")

try:
    # 3. Connection logic (Standard for all platforms)
    with serial.Serial(ARDUINO_PORT, 9600, timeout=1) as ser:
        while True:
            temp = round(random.uniform(20.0, 30.0), 2)
            hum = random.randint(30, 70)
            light = random.randint(0, 1023)

            payload = f"{temp},{hum},{light}\n"
            write_to_serial(ser, payload)

            print(f"Arduino Sent: {payload.strip()}")
            time.sleep(0.5)

except KeyboardInterrupt:
    print("\nShutting down...")
except serial.SerialException as e:
    print(f"\nSerial Error: {e}")
    print(f"Tip: On Windows, make sure {ARDUINO_PORT} exists (com0com).")
finally:
    if socat_process:
        socat_process.terminate()

import platform
import sys
import time

import serial

from data.sensors_data import (
    get_dist_cm,
    get_hum,
    get_lidar_m,
    get_light,
    get_soil_moist,
    get_temp,
)
from lib.open_socket import get_ports, open_socket


def start_simulation():
    # 1. Setup Virtual Bridge (Silent Background Task)
    terminal_output, socat_process = open_socket()

    if platform.system() == "Windows":
        ARDUINO_PORT, LISTENER_PORT = "COM1", "COM2"
    else:
        ports = get_ports(terminal_output)
        if len(ports) < 2:
            print("Error: Could not establish virtual serial bridge.")
            return
        ARDUINO_PORT, LISTENER_PORT = ports[0], ports[1]

    print(f"--- BRIDGE ACTIVE: Connect Analyzer to {LISTENER_PORT} ---")

    try:
        with serial.Serial(ARDUINO_PORT, 9600, timeout=1) as ser:
            # 2. Sensor Selection UI
            menu = {
                1: ("Temperature", get_temp),
                2: ("Humidity", get_hum),
                3: ("Light", get_light),
                4: ("Soil Moisture", get_soil_moist),
                5: ("Ultrasonic", get_dist_cm),
                6: ("Lidar", get_lidar_m),
            }

            selected_ids = []
            while True:
                print("\n" + "=" * 30)
                for k, v in menu.items():
                    status = "[SELECTED]" if k in selected_ids else ""
                    print(f"{k}. {v[0]} {status}")
                print("7. START DIFFUSION")

                try:
                    choice = int(input("\nSelect (1-7): "))
                    if choice == 7:
                        if not selected_ids:
                            continue
                        break
                    if 1 <= choice <= 6 and choice not in selected_ids:
                        selected_ids.append(choice)
                except ValueError:
                    continue

            # 3. Efficient Data Diffusion
            selected_ids.sort()
            # Send a Header first so the Analyzer knows the column names
            header = ",".join([menu[i][0] for i in selected_ids]) + "\n"
            ser.write(header.encode())

            print(f"\nStreaming: {header.strip()}")
            print("Press Ctrl+C to stop simulation.")

            while True:
                # Use a list comprehension for maximum efficiency
                readings = [str(menu[i][1]()) for i in selected_ids]
                payload = ",".join(readings) + "\n"

                ser.write(payload.encode("utf-8"))
                sys.stdout.write(f"\rSending: {payload.strip()}      ")
                sys.stdout.flush()
                time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")
    finally:
        if socat_process:
            socat_process.terminate()


if __name__ == "__main__":
    start_simulation()

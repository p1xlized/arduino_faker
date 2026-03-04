import os
import platform
import re
import subprocess

"""
Open a socket pair using socat.

:return: A tuple containing the output of socat and the process object.
"""


def open_socket():
    current_os = platform.system()

    if current_os == "Windows":
        # Windows doesn't have socat.
        # Realistically, you'd use a pre-existing pair like COM1/COM2
        # created by 'com0com'.
        return "WINDOWS_MODE: Use COM1 and COM2", None

    else:
        # Linux and macOS both support socat
        try:
            # Check if socat is installed
            subprocess.run(["socat", "-V"], capture_output=True, check=True)

            cmd = ["socat", "-d", "-d", "pty,raw,echo=0", "pty,raw,echo=0"]
            process = subprocess.Popen(cmd, stderr=subprocess.PIPE, text=True)

            output = ""
            # We read stderr because that's where socat logs its port info
            for _ in range(10):
                line = process.stderr.readline()  # pyright: ignore[reportOptionalMemberAccess]
                output += line
                if "starting data transfer" in line.lower():
                    break
            return output, process

        except (subprocess.CalledProcessError, FileNotFoundError):
            return (
                "ERROR: socat not found. Install via 'brew install socat' (Mac) or 'sudo apt install socat' (Linux)",
                None,
            )


"""
Get the port names from the socat output.

:param terminal_output: The output of socat.
:return: A list of port names.
"""


def get_ports(terminal_output):
    # Regex designed to find Linux pts AND Mac ttys
    pattern = r"/dev/(?:pts/\d+|ttys\d+)"
    return re.findall(pattern, str(terminal_output))

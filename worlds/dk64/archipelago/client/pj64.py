"""Contains the PJ64Client class for interacting with Project64."""

import socket
import json
import os
import pkgutil
from configparser import ConfigParser
import sys
import subprocess
from Utils import open_filename
from Utils import get_settings
import uuid

if __name__ == "__main__":
    Utils.init_logging("DK64Context", exception_logger="Client")
from CommonClient import logger


class PJ64Exception(Exception):
    """
    Custom exception class for PJ64-related errors.

    This exception is raised when an error specific to PJ64 operations occurs.

    Attributes:
        message (str): Explanation of the error.
    """

    pass


def display_error_box(title: str, text: str) -> bool | None:
    """Display an error message box."""
    from tkinter import Tk, messagebox

    root = Tk()
    root.withdraw()
    ret = messagebox.showerror(title, text)
    root.update()
    return ret


class PJ64Client:
    """PJ64Client is a class that provides an interface to connect to and interact with an N64 emulator."""

    def __init__(self):
        """Initialize a new instance of the class."""
        self._check_client()
        self.address = "127.0.0.1"
        self.socket = None
        self.connected_message = False
        try:
            self._connect()
        except PJ64Exception:  # Don't abort creating the client if we can't connect immediately. We can always retry connection.
            pass

    def _check_client(self):
        """Ensure the Project 64 executable and the required adapter script are properly set up.

        Raises:
            PJ64Exception: If the Project 64 executable is not found or if the `ap_adapter.js` file is in use.
        """
        logger.info("We HIGHLY recommend starting Project64 through the client to ensure the config file is set up correctly.")
        logger.info("If you have already started Project64, please close it and start it through the client.")
        logger.info("You may also need to run the client as an administrator to write the config file.")
        options = get_settings()
        executable = options.get("project64_options", {}).get("executable")
        # Verify the file exists, if it does not, ask the user to select it
        if executable and not os.path.isfile(executable):
            executable = None
        if not executable:
            executable = open_filename("Project 64 4.0 Executable", (("Project64 Executable", (".exe",)),), "Project64.exe")
            if not executable:
                raise PJ64Exception("Project 64 executable not found.")
            options.update({"project64_options": {"executable": executable}})
            options.save()

        # Check if the file ap_adapter exists in the subfolder of the executable, the folder Scripts
        # If it does not exist, copy it from worlds/dk64/client/adapter.js
        adapter_path = os.path.join(os.path.dirname(executable), "Scripts", "ap_adapter.js")
        # Read the existing file from the world
        try:
            with open("worlds/dk64/archipelago/client/adapter.js", "r", encoding="utf8", newline="\n") as f:
                adapter_content = f.read()
        except Exception:
            adapter_content = pkgutil.get_data(__name__, "adapter.js").decode().replace("\r\n", "\n").replace("\r", "\n")
        # Check if the file is in use
        matching_content = False
        # Check if the contents match
        try:
            with open(adapter_path, "r", encoding="utf8") as f:
                if f.read() == adapter_content:
                    matching_content = True
        except FileNotFoundError:
            pass
        if not matching_content:
            try:
                with open(adapter_path, "w", encoding="utf8") as f:
                    f.write(adapter_content)
            except PermissionError:
                display_error_box("Permission Error", "Unable to add adapter file to Project64, you may need to run AP as an administrator or close Project64.")
                raise PJ64Exception("Unable to add adapter file to Project64, you may need to run this script as an administrator or close Project64.")
        self._verify_pj64_config(os.path.join(os.path.dirname(executable), "Config", "Project64.cfg"))
        # Check if project 64 is running
        if not self._is_exe_running(os.path.basename(executable)):
            # Request the user to provide their ROM
            rom = open_filename("Select ROM", (("N64 ROM", (".n64", ".z64", ".v64")),))
            if rom:
                os.popen(f'"{executable}" "{rom}"')

    def _is_exe_running(self, exe_name):
        """Check if a given executable is running without using psutil."""
        exe_name = exe_name.lower()

        if sys.platform == "win32":
            try:
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                output = subprocess.check_output(["tasklist"], text=True, errors="ignore", shell=False, startupinfo=startupinfo)
                return exe_name in output.lower()
            except subprocess.CalledProcessError:
                return False

        else:  # Unix-based (Linux/macOS)
            try:
                result = subprocess.run(["pgrep", "-f", exe_name], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                return result.returncode == 0
            except FileNotFoundError:
                return False  # `pgrep` not available

        return False

    def _verify_pj64_config(self, config_file):
        """
        Verify and update the Project64 configuration file.

        - Cleans malformed lines from the file.
        - Ensures required sections and settings exist.
        - Prevents junk values from being added or re-written.
        """

        def clean_config_file(file_path):
            """Read the config file and return cleaned lines."""
            cleaned_lines = []

            def read_and_clean_lines(file_path, encoding):
                with open(file_path, encoding=encoding) as f:
                    for line in f:
                        stripped = line.strip()
                        if stripped == "" or stripped.startswith("[") or "=" in stripped:
                            cleaned_lines.append(line)

            try:
                read_and_clean_lines(file_path, "utf8")
            except UnicodeDecodeError:
                # Try one fallback encoding, just in case
                read_and_clean_lines(file_path, "latin1")
            return cleaned_lines

        def sanitize_config(config):
            """Remove invalid keys from the config object in memory."""
            for section in config.sections():
                keys_to_remove = [key for key in config[section] if not key.strip() or " " in key.strip() and "=" not in f"{key}=dummy"]
                for key in keys_to_remove:
                    config.remove_option(section, key)

        # Step 1: Clean the file and load cleaned data into ConfigParser
        try:
            cleaned_lines = clean_config_file(config_file)
            config = ConfigParser()
            config.read_string("".join(cleaned_lines))
        except Exception:
            raise PJ64Exception("Failed to read or clean the config file.")

        # Step 2: Sanitize the config in memory
        sanitize_config(config)

        # Step 3: Ensure required sections/settings
        if "Settings" not in config:
            config.add_section("Settings")
        config.set("Settings", "Basic Mode", "0")

        if "Debugger" not in config:
            config.add_section("Debugger")
        if not config.has_option("Debugger", "Debugger"):
            config.set("Debugger", "Debugger", "1")
        if not config.has_option("Debugger", "Autorun Scripts"):
            config.set("Debugger", "Autorun Scripts", "ap_adapter.js")
        first_set_port = False
        if not config.has_option("Debugger", "ap_port"):
            port = str(40000 + (uuid.uuid4().int % 10000))
            config.set("Debugger", "ap_port", port)
            first_set_port = True
            self.port = int(port)
            print("Set port to " + str(port))
        else:
            self.port = int(config.get("Debugger", "ap_port"))

        # Step 4: Final sanitize before write
        sanitize_config(config)
        # Print the config to the console for debugging
        print("Config file contents:")
        for section in config.sections():
            print(f"[{section}]")
            for key, value in config.items(section):
                print(f"{key} = {value}")
        # Step 5: Write config back to file
        try:
            with open(config_file, "w", encoding="utf8", newline="\n") as f:
                config.write(f, space_around_delimiters=False)
        except Exception:
            if first_set_port:
                raise PJ64Exception("Failed to update Project64 config file. If this is the first time set up of PJ64, you need to start PJ64 through the client to write the config file.")

    def _connect(self):
        """Establish a connection to the specified address and port using a socket.

        If the socket is not already created, it initializes a new socket with
        AF_INET and SOCK_STREAM parameters and sets a timeout of 0.1 seconds.
        Raises:
            PJ64Exception: If the connection is refused, reset, or aborted.
            OSError: If the socket is already connected.
        """
        if self.connected_message:
            return
        if self.socket is None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(0.1)
        try:
            self.socket.connect((self.address, self.port))
            self.connected_message = True
        except (ConnectionRefusedError, ConnectionResetError, ConnectionAbortedError) as e:
            self.socket = None
            self.connected_message = False
            print(e)
            raise PJ64Exception("Connection refused or reset")
        except OSError:
            # We're already connected, just move on
            pass

    def _send_command(self, command):
        """Send a command to the emulator and retrieves the response."""
        try:
            self._connect()
            command_id = str(uuid.uuid4())  # Generate a unique ID for the command
            full_command = f"{command_id}:{command}\n"  # Append line terminator
            self.socket.sendall(full_command.encode())

            response = self.socket.recv(8192).decode()
            if not response or len(str(response).strip()) == 0:
                raise PJ64Exception("No data received from the server")
            # Split response by line terminator and process each line
            for line in response.splitlines():
                if line.startswith(command_id):
                    data = line[len(command_id) :]
                    if data.startswith(":"):
                        data = data[1:]

                    return data  # Return the response after the ID

            # If no matching ID is found, raise an exception
            raise PJ64Exception("Response ID does not match the command ID")
        except socket.timeout:
            self.socket = None
            self.connected_message = False
            raise PJ64Exception(
                "Socket Timeout, please check that Project64 is running and the adapter is actively bound to a port.\nIf PJ64 fails to bind to a port, please update your Project64 config file with a new port."
            )
        except Exception as e:
            self.socket = None
            self.connected_message = False
            raise PJ64Exception(e)

    def _read_memory(self, address, size):
        """Read an unsigned integer of the given size from memory."""
        return int(self._send_command(f"read u{size * 8} {hex(address)} {size}"))

    def rominfo(self):
        """Retrieve ROM information from the emulator."""
        return json.loads(self._send_command("romInfo"))

    def read_u8(self, address):
        """Read an 8-bit unsigned integer from memory."""
        return self._read_memory(address, 1)

    def read_u16(self, address):
        """Read a 16-bit unsigned integer from memory."""
        return self._read_memory(address, 2)

    def read_u32(self, address):
        """Read a 32-bit unsigned integer from memory."""
        return self._read_memory(address, 4)

    def read_dict(self, dict):
        """Read a dictionary of memory addresses and returns the values."""
        return self._send_command(f"dict {json.dumps(dict, separators=(',', ':'))}")

    def read_bytestring(self, address, length):
        """Read a bytestring from memory."""
        return self._send_command(f"read bytestring {hex(address)} {length}")

    def _write_memory(self, command, address, data):
        """Write data to memory and returns the emulator response."""
        return self._send_command(f"{command} {hex(address)} {data}")

    def write_u8(self, address, data):
        """Write an 8-bit unsigned integer to memory."""
        return self._write_memory("write u8", address, [data])

    def write_u16(self, address, data):
        """Write a 16-bit unsigned integer to memory."""
        return self._write_memory("write u16", address, [data])

    def write_u32(self, address, data):
        """Write a 32-bit unsigned integer to memory."""
        return self._write_memory("write u32", address, [data])

    def write_bytestring(self, address, data):
        """Write a bytestring to memory."""
        return self._write_memory("write bytestring", address, str(data).upper() + "\x00")

    def validate_rom(self, name, memory_location=None):
        """Validate the ROM by comparing its name and optional memory location."""
        rom_info = self.rominfo()
        if not rom_info:
            return False
        if rom_info.get("goodName", "").upper() == name.upper():
            return memory_location is None or self.read_u32(memory_location) != 0
        return False

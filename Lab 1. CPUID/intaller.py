# file == bd os.tmpfile()
from sys import platform
from subprocess import check_output
import hashlib
import os


def get_CPUsum():
    if platform == "linux" or platform == "linux2" or platform == "win32": # "cat", "/proc/cpuinfo"
        # linux
        print("Sorry, but this program only for MacOS! ")
        return None
    elif platform == "darwin":
        # OS X
        output = check_output("system_profiler SPHardwareDataType | grep UUID", shell=True).decode()
        hard_uuid = output.split(":")[1][1:-1]
        output = check_output("system_profiler SPHardwareDataType | grep Serial", shell=True).decode()
        serial_num = output.split(":")[1][1:-1]
        check_str = hard_uuid + " " + serial_num
        return hashlib.sha256(check_str.encode('utf-8')).hexdigest()

def check_CPUsum(given_checksum):
    real_key = from_license_key()
    if real_key != get_CPUsum():
        return False
    else:
        return True

def to_license_key(checksum):
    with open("license.key", "w") as lic_file:
        lic_file.write(checksum)

def from_license_key():
    with open("license.key", "r") as lic_file:
        return lic_file.readline()

if __name__ == "__main__":
    #to_license_key(get_CPUsum())
    print(from_license_key())
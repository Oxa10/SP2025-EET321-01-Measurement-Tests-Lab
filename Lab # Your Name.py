# YOUR NAME
# EET321
# SECTION NUMBER
# ASSIGNMENT NAME
# DATE
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
install("pyvisa")

# Import libraries.
import pyvisa
import time
import csv
from datetime import datetime
rm = pyvisa.ResourceManager()


#Find power supply address
try:
    Powersupply = [a for a in rm.list_resources() if 'SPD' in a]
    supply = rm.open_resource(Powersupply[0])
except IndexError:
    print("PowerSupply not connected or powered on")

#Find DMM address
try:
    Digital = [b for b in rm.list_resources() if 'SDM' in b]
    dmm = rm.open_resource(Digital[0])
except IndexError:
    print("Digital MultiMeter not connected or powered on")

#Find Osilly address
try:
    OSilly = [c for c in rm.list_resources() if 'SDS' in c]
    oscope = rm.open_resource(OSilly[0])
except IndexError:
    print("Oscilloscope not connected or powered on")

#Find Function  address
try:
    Fuci = [d for d in rm.list_resources() if 'SDG' in d]
    fungen = rm.open_resource(Fuci[0])
except IndexError:
    print("Function Generator not connected or powered on")

oscope.timeout = 15000
# Define the CSV file
csv_filename = 'measurements.csv'


# Function to write header if the file is empty
def write_header():
    try:
        with open(csv_filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Measured Voltage"])
    except Exception as e:
        print(f"Error writing header to CSV: {e}")

    # Function to append data to CSV file


def append_to_csv(timestamp, measured_voltage):
    try:
        with open(csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, measured_voltage])
    except Exception as e:
        print(f"Error writing to CSV: {e}")

    # Measurements every 2 seconds


def main():
    # Write header if the file is new
    write_header()

    try:
        while True:
            measured_voltage = oscope.query("C1:PAVA? PWID")
            print(f"Oscilloscope Measured Voltage: {measured_voltage}")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            append_to_csv(timestamp, measured_voltage)
            time.sleep(2)
    except KeyboardInterrupt:
        print("Measurement stopped by user.")

    # Run


if __name__ == "__main__":
    main()



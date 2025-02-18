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

# Set the DMM for voltage measurement mode
dmm.write("CONF:VOLT:DC")

current = .01
measurements = []

import time
# Function to set the current on the DC power supply and set voltage to 32V
def set_test_current(current):
    supply.write("INST:SEL CURR")  # Set the supply to current mode (if needed)
    supply.write(f"CURR {current}")  # Set the test current
    supply.write("CH1:VOLTage 1")
    supply.write("OUTPut CH1,ON")
    time.sleep(1)  # Allow a moment for the supply to adjust


# Function to measure voltage with the DMM
def measure_voltage_dmm():
    try:
        return float(dmm.query("MEAS:VOLT:DC?"))
    except pyvisa.errors.VisaIOError as e:
        print(f"Error with DMM: {e}")
        return None


# Function to execute the test sequence
def run_tests():
    current=.01
    while current<2:
        set_test_current(current)
        print(f"Setting test current: {current} A, Voltage: 32V")

        # Stabilization loop with alternating output states
        print("Waiting 30 seconds for temperature stabilization...")
        supply.write("OUTPut CH1,OFF")
        time.sleep(5)
        supply.write("OUTPut CH1,ON")
        time.sleep(5)
        current = current * 10

        # Measure the voltage drop using the DMM
        measured_voltage = measure_voltage_dmm()
        if measured_voltage is not None:
            resistance = measured_voltage / current  # Calculate resistance
            measurements.append([current, measured_voltage, resistance])
            print(f"Measured voltage: {measured_voltage} V, calc. resistance: {resistance} Ω")

        else:
            print("Error, measurement failed.")


# Run the tests
run_tests()
import csv
# Save the results to a CSV file
with open('resistance_measurements.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Test Current (A)', 'Measured Voltage (V)', 'Calculated Resistance (Ohms)'])
    writer.writerows(measurements)

supply.write("OUTPut CH1,OFF")
print("Test complete. Results saved to 'resistance_measurements.csv'.")

# YOUR NAME
# EET321
# SECTION NUMBER
# ASSIGNMENT NAME
# DATE

import subprocess
import sys
import time
import csv
import pyvisa


# Function to install required package if not already installed
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


install("pyvisa")

# Initialize VISA resource manager
rm = pyvisa.ResourceManager()


# Function to find instrument by identifier
def find_instrument(identifier):
    try:
        instrument = [addr for addr in rm.list_resources() if identifier in addr]
        return rm.open_resource(instrument[0]) if instrument else None
    except Exception as e:
        print(f"Error finding {identifier}: {e}")
        return None


# Detect and connect to instruments
supply = find_instrument('SPD')  # Power Supply
if not supply:
    print("Power Supply not connected or powered on")

dmm = find_instrument('SDM')  # Digital Multimeter
if not dmm:
    print("Digital Multimeter not connected or powered on")

oscope = find_instrument('SDS')  # oSILLY
if not oscope:
    print("Oscilloscope not connected or powered on")

fungen = find_instrument('SDG')  # Function Generator
if not fungen:
    print("Function Generator not connected or powered on")

# Configure the DMM for DC voltage measurement
if dmm:
    dmm.write("CONF:VOLT:DC")


# Function to set the test current and enable the power supply
def set_test_current(current):
    if supply:
        try:
            supply.write("INST:SEL CURR")  # Set to current mode
            supply.write(f"CURR {current}")  # Set the current
            supply.write("CH1:VOLT 1")  # Set voltage to 1V
            supply.write("OUTPut CH1,ON")  # Turn on output
            time.sleep(1)  # Allow stabilization
        except Exception as e:
            print(f"Error setting current: {e}")


# Function to measure voltage from the DMM
def measure_voltage_dmm():
    if dmm:
        try:
            return float(dmm.query("MEAS:VOLT:DC?"))
        except pyvisa.errors.VisaIOError as e:
            print(f"Error with DMM measurement: {e}")
            return None
    return None


# Function to execute the test sequence
def run_tests():
    measurements = []
    current = 0.01  # Start with 10mA
    while current < 2:
        set_test_current(current)
        print(f"Setting test current: {current} A, Voltage: 32V")

        # Temperature stabilization delay
        print("Waiting 30 seconds for temperature stabilization...")
        if supply:
            supply.write("OUTPut CH1,OFF")
            time.sleep(5)
            supply.write("OUTPut CH1,ON")
            time.sleep(5)

        # Measure the voltage drop using the DMM
        measured_voltage = measure_voltage_dmm()
        if measured_voltage is not None:
            resistance = measured_voltage / current  # Calculate resistance
            measurements.append([current, measured_voltage, resistance])
            print(f"Measured voltage: {measured_voltage} V, Calculated resistance: {resistance} Ω")
        else:
            print("Error: Measurement failed.")

        # Increase the current for the next iteration
        current *= 10

    return measurements


# Run the tests and collect results
measurements = run_tests()

# Save results to a CSV file
with open('resistance_measurements.csv', mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Current (A)', 'Measured Voltage (V)', 'Calculated Resistance (Ohms)'])
    writer.writerows(measurements)

# Turn off the power supply after tests
if supply:
    supply.write("OUTPut CH1,OFF")

print("Test complete. Results saved to 'resistance_measurements.csv'.")

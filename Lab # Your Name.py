# Clark Sarge
# EET321
# 1
# Lab 2 Resistance Measurement
# 2/18/2025
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
install("pyvisa")

# Import libraries.
import time
import pyvisa

rm = pyvisa.ResourceManager()

#Find power supply address
try:
    Powersupply = [a for a in rm.list_resources() if 'SPD' in a]
    PSU = rm.open_resource(Powersupply[0])
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


# Set the DMM for voltage
dmm.write("CONF:VOLT:DC")

#(10mA, 100mA, 1A)
test_currents = [0.01, 0.1, 1]
measurements = []

# Function to set the current
def set_test_current(current):
    PSU.write("INST:SEL CURR")
    PSU.write(f"CURR {current}")
    PSU.write("CH1:VOLTage 10")
    PSU.write("OUTPut CH1,ON")
    time.sleep(1)

#measure voltage with the DMM
def measure_voltage_dmm():
    try:
        voltage = float(dmm.query("MEAS:VOLT:DC?"))
        return voltage
    except pyvisa.errors.VisaIOError as e:
        print(f"Error with DMM: {e}")
        return None

def run_tests():
    #Set to 1V
    for current in test_currents:
        set_test_current(current)
        print(f"Setting test current: {current} A, Voltage: 1V")

        #Wait 2 minutes
        print("Waiting 2 minutes for temperature stabilization...")
        PSU.write(f"CURR {current}")
        PSU.write("OUTPut CH1,OFF")
        time.sleep(120)
        PSU.write("OUTPut CH1,ON")

        #Measure the voltage drop
        measured_voltage = measure_voltage_dmm()
        if measured_voltage is not None:
            #Calc. the resistance
            resistance = measured_voltage / current
            measurements.append([current, measured_voltage, resistance])
            print(f"Measured voltage: {measured_voltage} V, calc. resistance: {resistance} Ω")
        else:
            print("Error, measurement failed.")

run_tests()

#Save results
with open('resistance_measurements.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Test Current (A)', 'Measured Voltage (V)', 'Calculated Resistance (Ohms)'])
    writer.writerows(measurements)

#finished test
PSU.write("OUTPut CH1,OFF")
print("Test complete. Results saved to 'resistance_measurements.csv'.")
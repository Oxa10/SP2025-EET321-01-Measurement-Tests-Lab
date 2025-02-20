# Joseph Bower
# EET321
# 1
# Lab 2
# 2/18/2025
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
install("pyvisa")

# Import libraries.
import pyvisa
import time
import csv

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


#Create a list of measured values.
measurements = []

#Start program by turning off power supply and setting it to 1 volt.
supply.write("OUTPut CH1,OFF")
supply.write("CH1:VOLTage 1")
time.sleep(1)


amp_settings = [0.01, 0.1, 1]

#Set current values and take measurements.
for amp in amp_settings:
    supply.write("OUTPut CH1,ON")
    com = "CH1:CURRent " + str(amp)
    supply.write(com)
    time.sleep(1)
    volts = float(dmm.query("MEAS:VOLT:DC?"))
    resist = volts/amp
    measurements.append([str(amp),str(volts),str(resist)])
    supply.write("OUTPut CH1,OFF")
    time.sleep(120)

# Save data to a CSV file
with open('test_measurements.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(
        ['Test Current(A)', 'Measured Voltage(V)', 'Calculated Resistance (Ω)'])
    writer.writerows(measurements)
print("Test complete. Results saved to 'test_measurements.csv'.")  # End test print cmd
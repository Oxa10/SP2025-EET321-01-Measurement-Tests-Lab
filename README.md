# SP2025-EET321-01-Measurement-Tests-Lab
Where SP2025 EET321-01 Measurement &amp; Tests Lab stores code
DO NOT UPLOAD TO MAIN, IF MAIN IS BORKED BACK UP IS BELLOW

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
    PS1 = Powersupply[0]
    supply = rm.open_resource(PS1)
except IndexError:
    print("PowerSupply not connected or powered on")

#Find DMM address
try:
    Digital = [b for b in rm.list_resources() if 'SDM' in b]
    DMM1 = Digital[0]
    dmm = rm.open_resource(DMM1)
except IndexError:
    print("Digital MultiMeter not connected or powered on")

#Find Osilly address
try:
    OSilly = [c for c in rm.list_resources() if 'SDS' in c]
    OS1 = OSilly[0]
    oscope = rm.open_resource(OS1)
except IndexError:
    print("Oscilloscope not connected or powered on")

#Find Function  address
try:
    Fuci = [d for d in rm.list_resources() if 'SDG' in d]
    FG1 = Fuci[0]
    fungen = rm.open_resource(FG1)
except IndexError:
    print("Function Generator not connected or powered on")

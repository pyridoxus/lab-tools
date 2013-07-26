'''
Created on Jul 3, 2013

@author: cmcculloch
'''

from powerSupplies import PowerSupplyInstekPsm6003
from dmms import DmmKeithley2750
from functionGenerators import FunctionGeneratorsAgilent33220A
from dcSources import DcSourcesKrohnHiteEdc523
import random

from time import sleep
if __name__ == "__main__":
    loop = 0
    powerSupply = PowerSupplyInstekPsm6003("172.24.24.30", "gpib0,9", 1)
    dmm = DmmKeithley2750("172.24.24.30", "gpib0,16", 1)
    fgen = FunctionGeneratorsAgilent33220A("172.24.24.30", "gpib0,10", 1)
    dcsource = DcSourcesKrohnHiteEdc523("172.24.24.30", "gpib0,2", 1)
    while True:
        loop += 1
        print "**********************************************************", loop
        powerSupply.setVoltage(random.randint(4, 16), 2, 2)
        sleep(10)
        powerSupply.inputOff()
    
        dmm.setDcVoltsMode()
        print dmm.takeMeasurement()
        dmm.setAcVoltsMode()
        print dmm.takeMeasurement()
        dmm.setDcCurrentMode()
        print dmm.takeMeasurement()
        dmm.set2WireResistanceMode()
        print dmm.takeMeasurement()
        dmm.set4WireResistanceMode()
        print dmm.takeMeasurement()
        dmm.setFrequencyMode()
        print dmm.takeMeasurement()
    
        fgen.setSineWave(-random.random(), random.random(), random.randint(1, 1000))
    
        dcsource.setDcVoltage(random.random())
    

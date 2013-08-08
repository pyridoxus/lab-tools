'''
Created on Jul 3, 2013

@author: cmcculloch
'''

from powerSupplies import PowerSupplyInstekPsm6003
from dmms import DmmKeithley2750
from functionGenerators import FunctionGeneratorsAgilent33220A
from dcSources import DcSourcesKrohnHiteEdc523
from electronicLoads import EloadTexio151_201
from switchMatrices import SwitchMatrixKeithley2750

import random

from time import sleep
if __name__ == "__main__":
    loop = 0
    powerSupply = PowerSupplyInstekPsm6003("172.24.24.30", "gpib0,9", 1)
    dmm = DmmKeithley2750("172.24.24.30", "gpib0,16", 1)
    fgen = FunctionGeneratorsAgilent33220A("172.24.24.30", "gpib0,10", 1)
    dcsource = DcSourcesKrohnHiteEdc523("172.24.24.30", "gpib0,2", 1)
    eload = EloadTexio151_201("172.24.24.30", "gpib0,13", 1)
    switchMatrix = SwitchMatrixKeithley2750("172.24.24.30", "gpib0,16", 1)
    while True:
        loop += 1
        print "**********************************************************", loop
#         powerSupply.setVoltage(random.randint(4, 16), 2, 2)

        dcsource.crowBar("OFF")
        dmm.setDcVoltsMode()
        switchMatrix.closeSwitch("DMM", (1, 1))
        switchMatrix.closeSwitch("DCSOURCE", (1, 3))
        v = random.random()
        dcsource.setDcVoltage(v)
        sleep(2)
        print "dmm  : ", dmm.takeMeasurement(), " DC volts"
        print "ideal: ", v
        dcsource.crowBar("ON")
        switchMatrix.openAllSwitches()
        sleep(1)
        
        dmm.setAcVoltsMode()
        switchMatrix.closeSwitch("DMM", (1, 1))
        switchMatrix.closeSwitch("FGEN", (1, 3))
        v = random.random()
        fgen.setSineWave(-v, v, random.randint(1, 1000))
        sleep(2)
        print "dmm  : ", dmm.takeMeasurement(), " AC volts"
        print "ideal: ", v / 2
        switchMatrix.openAllSwitches()
        sleep(1)
        
        dmm.setFrequencyMode()
        switchMatrix.closeSwitch("DMM", (1, 1))
        switchMatrix.closeSwitch("FGEN", (1, 3))
        v = random.randint(1, 1000)
        fgen.setSineWave(-1, 1, v)
        sleep(2)
        print "dmm  : ", dmm.takeMeasurement(), " Hertz"
        print "ideal: ", v
        switchMatrix.openAllSwitches()
        sleep(1)
        
#         dmm.setAcVoltsMode()
#         print dmm.takeMeasurement()
#         dmm.setDcCurrentMode()
#         print dmm.takeMeasurement()
#         dmm.set2WireResistanceMode()
#         print dmm.takeMeasurement()
#         dmm.set4WireResistanceMode()
#         print dmm.takeMeasurement()
#         dmm.setFrequencyMode()
#         print dmm.takeMeasurement()
#     
#         fgen.setSineWave(-random.random(), random.random(), random.randint(1, 1000))
#     
#         dcsource.setDcVoltage(random.random())
        eload.setCurrentMode(random.random())
        eload.inputOn()
        sleep(1)
        print "eload on: ", eload.measureCurrent()
        print "Power supply loaded: ", powerSupply.measureCurrent()
        eload.inputOff()
        sleep(1)
        print "eload off: ", eload.measureCurrent()
        print "Power supply unloaded: ", powerSupply.measureCurrent()
        powerSupply.inputOff()

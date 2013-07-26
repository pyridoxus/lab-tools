'''
Created on Jul 3, 2013

@author: cmcculloch
'''

from powerSupplies import PowerSupplyInstekPsm6003
from dmms import DmmKeithley2750
from functionGenerators import FunctionGeneratorsAgilent33220A
from dcSources import DcSourcesKrohnHiteEdc523

from time import sleep
if __name__ == "__main__":
#     powerSupply = PowerSupplyInstekPsm6003("172.24.24.30", "gpib0,9", 1)
#     powerSupply.setVoltage(12, 2, 2)
#     sleep(10)
#     powerSupply.inputOff()
    
    dmm = DmmKeithley2750("172.24.24.30", "gpib0,16", 1)
    dmm.setDcVoltsMode()
    print dmm.takeMeasurement()
    dmm.setAcVoltsMode()
    print dmm.takeMeasurement()
    dmm.setDcCurrentMode()
    print dmm.takeMeasurement()
    
#     fgen = FunctionGeneratorsAgilent33220A("172.24.24.30", "gpib0,10", 1)
#     fgen.setSineWave(-1, 1, 1000)
    
    dcsource = DcSourcesKrohnHiteEdc523("172.24.24.30", "gpib0,2", 1)
    print dcsource.setDcVoltage(1)
    

'''
Created on Jul 3, 2013

@author: cmcculloch
'''

from powerSupplies import PowerSupplyInstekPsm6003
from time import sleep
if __name__ == "__main__":
    powerSupply = PowerSupplyInstekPsm6003("172.24.24.30", "gpib0,9", 1)
    powerSupply.setVoltage(12, 2, 2)
    sleep(10)
    powerSupply.inputOff()
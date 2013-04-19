'''
Created on Apr 12, 2013

@author: cmcculloch
'''

from data_acquisition.vxi_11 import vxi_11_connection

class Keithley2750(vxi_11_connection):
    '''
    Define a simple interface to a Keithley 2750.
    '''
    def __init__(self):
        '''
        Initialize the object
        '''
        self.__idn = ""
        
        
    def getIDN(self):
        '''
        Print the IDN information.
        '''
        print self.__idn
        

if __name__ == "__main__":
    dmm = Keithley2750(host="172.24.24.30", 
             device="gpib0,16",  timeout=5000, device_name="Keithley 2750",
            raise_on_err=1)
    
    dmm.getIDN()
    
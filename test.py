'''
Created on Apr 12, 2013

@author: cmcculloch
'''

from data_acquisition.vxi_11 import vxi_11_connection
from data_acquisition.rpc import PMAP_PORT

class Keithley2750(vxi_11_connection):
    '''
    Define a simple interface to a Keithley 2750.
    '''
    def __init__(self, host = '127.0.0.1', device = "inst0", timeout = 1000,
                raise_on_err = None, device_name="Keithley 2750",
                shortname = None, portmap_proxy_host = None,
                portmap_proxy_port = PMAP_PORT):
        '''
        Initialize the object
        '''
        # idn_head is used to check that the correct instrument is at the
        # correct GPIB address. This check is done in the constructor of
        # vxi_11_connection.
        self.idn_head = "KEITHLEY INSTRUMENTS"
         
        vxi_11_connection.__init__(self, host, device, timeout, raise_on_err,
                                   device_name, shortname, portmap_proxy_host,
                                   portmap_proxy_port)
        
        
    def getIDN(self):
        '''
        Print the IDN information.
        '''
        print self.idn
        

class Agilent33220A(vxi_11_connection):
    '''
    Define a simple interface to an Agilent Technologies,33220A.
    '''
    def __init__(self, host = '127.0.0.1', device = "inst0", timeout = 1000,
                raise_on_err = None, device_name="Agilent Technologies,33220A",
                shortname = None, portmap_proxy_host = None,
                portmap_proxy_port = PMAP_PORT):
        '''
        Initialize the object
        '''
        # idn_head is used to check that the correct instrument is at the
        # correct GPIB address. This check is done in the constructor of
        # vxi_11_connection.
        self.idn_head = "Agilent Technologies,33220A"
         
        vxi_11_connection.__init__(self, host, device, timeout, raise_on_err,
                                   device_name, shortname, portmap_proxy_host,
                                   portmap_proxy_port)
        
        
    def getIDN(self):
        '''
        Print the IDN information.
        '''
        print self.idn
        

class KrohnHite523(vxi_11_connection):
    '''
    Define a simple interface to a Krohn-Hite, Model 523.
    '''
    def __init__(self, host = '127.0.0.1', device = "inst0", timeout = 1000,
                raise_on_err = None, device_name="Krohn-Hite, Model 523",
                shortname = None, portmap_proxy_host = None,
                portmap_proxy_port = PMAP_PORT):
        '''
        Initialize the object
        '''
        # idn_head is used to check that the correct instrument is at the
        # correct GPIB address. This check is done in the constructor of
        # vxi_11_connection.
        self.idn_head = "Krohn-Hite, Model 523"
         
        vxi_11_connection.__init__(self, host, device, timeout, raise_on_err,
                                   device_name, shortname, portmap_proxy_host,
                                   portmap_proxy_port)
        
        
    def getIDN(self):
        '''
        Print the IDN information.
        '''
        print self.idn
        

if __name__ == "__main__":
    dmm = Keithley2750(host="172.24.24.30", 
             device="gpib0,16",  timeout=5000, raise_on_err=1)
    
    dmm.getIDN()

    fgen = Agilent33220A(host="172.24.24.30", 
             device="gpib0,10",  timeout=5000, raise_on_err=1)
    
    fgen.getIDN()
 
    dcsource = KrohnHite523(host="172.24.24.30", 
             device="gpib0,2",  timeout=5000, raise_on_err=1)
    
    dcsource.getIDN()
   
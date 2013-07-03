'''
Base abstract instrument classes to join all Vendor and SoMat instrument objects

This must become a piece of CTHULU.
'''
import socket
from vendor.vxi_11 import vxi_11_connection
from vendor.rpc import PMAP_PORT
     
def getHwAddr(interface, host, port = 80):
    '''
    Get the MAC address of the device at the host IP address.
    Return None if no connection can be made (either bad IP or bad port)
    Return "INVALID" if no MAC address can be found.
    Return a valid MAC address if it is found.
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Connect to remote server to refresh the ARP file
    try:
        s.connect((host , port))
    except socket.error:
        return None
    
    arpFile = open("/proc/net/arp", 'r')
    
    mac = "INVALID"
    itemList = None
    for line in arpFile:
        if interface in line:
            if host in line:
                itemList = line.split(" ")
                break
    arpFile.close()

    if itemList is not None:
        for item in itemList:
            # Go through all pieces of the line and find the MAC address
            # It's the only item with a colon.
            if ":" in item:
                mac = item
    return mac
    


class VXIConnection(vxi_11_connection):
    '''
    Define a simple interface to GPIB VXI.
    '''
    def __init__(self, host = '127.0.0.1', device = "inst0", timeout = 1000,
                raise_on_err = None, device_name="None",
                shortname = None, portmap_proxy_host = None,
                portmap_proxy_port = PMAP_PORT):
        '''
        Initialize the object
        '''
        vxi_11_connection.__init__(self, host, device, timeout, raise_on_err,
                                   device_name, shortname, portmap_proxy_host,
                                   portmap_proxy_port)
        
        

class Instrument(object):
    '''
    Base instrument class.
    '''
    def _getUniqueIdent(self):
        ''' To be implemented by child classes. '''
        raise NotImplementedError, self



class gpibInstrument(Instrument):
    '''
    Subclass of instrument for GPIB type classes.
    '''
    
    def __init__(self, deviceName):
        ''' Set up the VXI connection. '''
        self.__vxi = VXIConnection(device_name = deviceName)


    def _getUniqueIdent(self, instrObj):
        ''' Return the result of asking the instrument for its ID. '''
        gpibIdent = instrObj.target.ask("*IDN?")
        
        manufSN = gpibIdent.split(",")[2]
        
        return manufSN



class ethernetInstrument(Instrument):
    '''
    Subclass of instrument for Ethernet type classes.
    '''
    def _getUniqueIdent(self, instrObj):
        '''
        Return the MAC address of the instrument.
        '''
        macIdent = getHwAddr(instrObj.ip_address)
        
        return macIdent



if __name__ == "__main__":
    print getHwAddr("eth0", "172.24.24.40")
    print getHwAddr("eth0", "172.24.24.30")
    print getHwAddr("eth0", "172.24.24.20")
    print getHwAddr("eth0", "172.24.24.25")    
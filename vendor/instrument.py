'''
Base abstract instrument classes to join all Vendor and SoMat instrument objects

This must become a piece of CTHULU.
'''

def getMACAddress(host):
    """ Returns the MAC address of a network host, requires >= WIN2K. """
    
    import ctypes
    import socket
    import struct
    # Check for api availability
    try:
        SendARP = ctypes.windll.Iphlpapi.SendARP
    except:
        raise NotImplementedError('Usage only on Windows 2000 and above')
        
    # Doesn't work with loopbacks, but let's try and help.
    if host == '127.0.0.1' or host.lower() == 'localhost':
        host = socket.gethostname()
    
    # gethostbyname blocks, so use it wisely.
    try:
        inetaddr = ctypes.windll.wsock32.inet_addr(host)
        if inetaddr in (0, -1):
            raise Exception
    except:
        hostip = socket.gethostbyname(host)
        inetaddr = ctypes.windll.wsock32.inet_addr(hostip)
    
    buff = ctypes.c_buffer(6)
    addlen = ctypes.c_ulong(ctypes.sizeof(buff))
    if SendARP(inetaddr, 0, ctypes.byref(buff), ctypes.byref(addlen)) != 0:
        raise 'Retrieval of mac address(%s) - failed' % host
    
    # Convert binary data into a string.
    macaddr = ''
    for intval in struct.unpack('BBBBBB', buff):
        if intval > 15:
            replacestr = '0x'
        else:
            replacestr = 'x'
        macaddr = ''.join([macaddr, hex(intval).replace(replacestr, '')])
    
    return macaddr.upper()

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
        macIdent = getMACAddress(instrObj.ip_address)
        
        return macIdent



if __name__ == "__main__":
    print getMACAddress("172.24.24.40")
